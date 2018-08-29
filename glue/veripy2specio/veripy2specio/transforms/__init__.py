import markdown2

from veripy2specio import constants


class Veripy2SpecioTransform(object):
    """ A general transformation class that converts data from the VeriPy
    (cucumber.json) format into a Specio format for later user by a templating
    engine or further processing.

    **Sample Usage**
    ::
        veripy_input, config = get_input_and_config()
        transform = Veripy2SpecioTransform(config)
        specio_output = transform(veripy_input)

    **Subclassing Notes**
    Methods are broken up into sub-generators for easily modified behavior.
    Typically, the methods take the form <element>_from_<parent_element>
    and return a generator.
    """

    def __init__(self, config):
        self.config = config

    def __call__(self, input):
        return {
            'organization': {},
            'features': [feature for feature in self.features_from_input(input)],
        }

    # Transformation Methods

    def group_steps(self, steps):
        """ Given a list of steps, group them into 2 bins: given_when and then
        based on their keyword.

        AND/BUT statements are lumped in with their predecesor.
        """
        groups = []
        switch = '--invalid--'

        for step in steps:
            step_type = step['step_type']

            if step_type in switch:
                # We're in the same state as last iteration. Do nothing
                pass
            elif step_type in (constants.GIVEN, constants.WHEN):
                # GIVEN/WHEN: Toggle the switch and push a new group onto the list.
                switch = 'given_when'
                groups.append({ 'given_when': [], 'then': []})
            elif step_type == constants.THEN:
                # THEN: Toggle the switch
                switch = 'then'
            else:
                # AND/BUT: Do nothing
                pass

            # Add the current step to the ending group.
            groups[-1][switch].append(step)

        return groups

    def description_from_feature(self, feature):
        """ Trim off the injected <pre> tags and parse the description
        as markdown.
        """
        return markdown2.markdown(feature.pop('description')[5:-6])

    def attachments_from_embeddings(self, embeddings):
        for embedding in embeddings:
            yield {}

    def passed_from_step(self, steps):
        for step in steps:
            yield step['passed']

    def steps_from_element(self, element):
        for step in element.pop('steps'):
            embeddings = step.pop('embeddings', [])
            yield {
                'passed': step['result']['status'] == constants.PASSED,
                'attachments': [
                    attachment
                    for attachment in
                    self.attachments_from_embeddings(embeddings)
                ],
                **step,
            }

    def tags_from_scenarios(self, scenarios):
        for scenario in scenarios:
            tags = scenario['tags']
            for tag in tags:
                yield tag['name']

    def scenarios_from_feature(self, feature):
        for i, element in enumerate(feature.pop('elements')):
            steps = [step for step in self.steps_from_element(element)]
            passed = all(self.passed_from_step(steps))
            tags = [tag for tag in self.tags_from_scenarios([element])]
            yield {
                'number': i + 1,
                'all_passed': passed,
                'steps': self.group_steps(steps),
                'tags': tags,
                **element,
            }

    def features_from_input(self, input):
        """ Given an input VeriPy file, retrieve the Specio formatted features.

        This function returns an iterable generator that can be used to progressively
        parse the input configuration.
        """
        for feature in input:
            scenarios = [scenario for scenario in self.scenarios_from_feature(feature)]
            scenario_tags = [tag for tag in self.tags_from_scenarios(scenarios)]
            yield {
                'description': self.description_from_feature(feature),
                'scenarios': scenarios,
                'scenario_tags': scenario_tags,
                **feature,
            }

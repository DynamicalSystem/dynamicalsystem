from dynamicalsystem.pytests.environment import variables as environment_variables


def test_notion(environment_variables):
    from dynamicalsystem.poohsticks.notion import Notion

    notion = Notion("tQ24.5", 100)
    assert notion.validate_content()

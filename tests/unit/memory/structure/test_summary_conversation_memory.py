import json
from griptape.summarizers import PromptDriverSummarizer
from griptape.memory.structure import SummaryConversationMemory, Run
from tests.mocks.mock_prompt_driver import MockPromptDriver
from griptape.tasks import PromptTask
from griptape.structures import Pipeline


class TestSummaryConversationMemory:
    def test_unsummarized_subtasks(self):
        memory = SummaryConversationMemory(offset=1, summarizer=PromptDriverSummarizer(driver=MockPromptDriver()))

        pipeline = Pipeline(memory=memory, prompt_driver=MockPromptDriver())

        pipeline.add_tasks(
            PromptTask("test")
        )

        pipeline.run()
        pipeline.run()
        pipeline.run()
        pipeline.run()

        assert len(memory.unsummarized_runs()) == 1

    def test_after_run(self):
        memory = SummaryConversationMemory(offset=1, summarizer=PromptDriverSummarizer(driver=MockPromptDriver()))

        pipeline = Pipeline(memory=memory, prompt_driver=MockPromptDriver())

        pipeline.add_tasks(
            PromptTask("test")
        )

        pipeline.run()
        pipeline.run()
        pipeline.run()
        pipeline.run()

        assert memory.summary is not None
        assert memory.summary_index == 3

    def test_to_json(self):
        memory = SummaryConversationMemory()
        memory.add_run(Run(input="foo", output="bar"))

        assert json.loads(memory.to_json())["type"] == "SummaryConversationMemory"
        assert json.loads(memory.to_json())["runs"][0]["input"] == "foo"

    def test_to_dict(self):
        memory = SummaryConversationMemory()
        memory.add_run(Run(input="foo", output="bar"))

        assert memory.to_dict()["type"] == "SummaryConversationMemory"
        assert memory.to_dict()["runs"][0]["input"] == "foo"

    def test_from_dict(self):
        memory = SummaryConversationMemory()
        memory.add_run(Run(input="foo", output="bar"))
        memory_dict = memory.to_dict()

        assert isinstance(memory.from_dict(memory_dict), SummaryConversationMemory)
        assert memory.from_dict(memory_dict).runs[0].input == "foo"

    def test_from_json(self):
        memory = SummaryConversationMemory()
        memory.add_run(Run(input="foo", output="bar"))
        memory_dict = memory.to_dict()

        assert isinstance(memory.from_dict(memory_dict), SummaryConversationMemory)
        assert memory.from_dict(memory_dict).runs[0].input == "foo"

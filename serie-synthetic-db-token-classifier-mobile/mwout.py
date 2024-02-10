import json
import datasets

logger = datasets.logging.get_logger(__name__)

_URL = "https://huggingface.co/datasets/alfarruggia/wmout/raw/main/"


class MWOUTConfig(datasets.BuilderConfig):
    """The MWOUT is a Workout Entity Dataset. """

    def __init__(self, **kwargs):
        """BuilderConfig for MWOUT.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MWOUTConfig, self).__init__(**kwargs)


class MWOUT(datasets.GeneratorBasedBuilder):
    """The MWOUT is a Workout Entity Dataset."""

    BUILDER_CONFIGS = [
        MWOUTConfig(
            name="mwout", version=datasets.Version("0.1.0"), description="The MWOUT is a Workout Entity Dataset."
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="_DESCRIPTION",
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=["B-Duration", "B-Workout", "I-Duration", "I-Frequency", "I-Workout", "0", "B-Frequency", "B-Number"]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/Arfius/motivation_workout/tree/main",
            citation="_CITATION",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": _URL+"train.json.zip",
            "validation": _URL+"validation.json.zip",
            "test": _URL+"test.json.zip"
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["validation"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        file = open(filepath)
        dataset_json = json.loads(file.read())
        for sentence_obj in dataset_json:
            if sentence_obj:
                yield int(sentence_obj['id']), sentence_obj
import supervisely as sly
import os
from glob import glob
import imagesize
from tqdm import tqdm


def create_ann(img_path):
    width, height = imagesize.get(img_path)
    img_tags = ann_dict.get(sly.fs.get_file_name(img_path))
    return sly.Annotation(img_size=(height, width), labels=[], img_tags=img_tags)


tag_names = ["id", "predominant_stress", "miner", "rust", "phoma", "cercospora", "severity"]
tag_metas = [
    (
        sly.TagMeta(name, sly.TagValueType.NONE)
        if 2 <= i <= 5
        else sly.TagMeta(name, sly.TagValueType.ANY_STRING)
    )
    for i, name in enumerate(tag_names)
]

ann_dict = {}


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    project = api.project.create(workspace_id, project_name)
    project_meta = sly.ProjectMeta(None, tag_metas)
    project_meta = api.project.update_meta(project.id, project_meta.to_json())

    dataset_path = "/mnt/c/users/german/documents/coffee-datasets/leaf/images"

    csv_path = os.path.dirname(dataset_path) + "/dataset.csv"
    with open(csv_path) as f:
        for line in f.readlines()[1:]:
            line_parts = line.strip().split(",")
            tags = []
            for i, value in enumerate(line_parts):
                if 2 <= i <= 5:
                    if value == "1":
                        tags.append(sly.Tag(tag_metas[i]))
                else:
                    tags.append(sly.Tag(tag_metas[i], value))
            ann_dict[line_parts[0]] = tags

    dataset = api.dataset.create(project.id, "ds0")
    img_paths = glob(dataset_path + "/*")
    for img_paths_batch in sly.batched(img_paths):
        img_names_batch = [sly.fs.get_file_name_with_ext(path) for path in img_paths_batch]
        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_paths_batch)
        img_ids = [img_info.id for img_info in img_infos]
        anns = [create_ann(img_path) for img_path in img_paths_batch]
        api.annotation.upload_anns(img_ids, anns)

    return project

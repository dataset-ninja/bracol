import supervisely as sly
import os
import csv
from glob import glob
import imagesize
from tqdm import tqdm


def create_annotation(image_path, annotation_dictionary):
    width, height = imagesize.get(image_path)
    image_tags = annotation_dictionary.get(sly.fs.get_file_name(image_path))
    return sly.Annotation(img_size=(height, width), labels=[], img_tags=image_tags)


def read_dataset_tags(csv_file_path, tag_meta_list):
    annotations = {}
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header line
        for row in reader:
            tags = []
            for index, value in enumerate(row):
                if 2 <= index <= 5:
                    if value == "1":
                        tags.append(sly.Tag(tag_meta_list[index]))
                elif index == 6:
                    if value == "0":
                        tags.append(sly.Tag(tag_meta_list[7]))
                else:
                    tags.append(sly.Tag(tag_meta_list[index], value))
            annotations[row[0]] = tags
    return annotations


def convert_and_upload_to_supervisely(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    tag_meta_names = [
        "id",
        "predominant_stress",
        "miner",
        "rust",
        "phoma",
        "cercospora",
        "severity",
        "healthy",
    ]
    tag_meta_list = [
        sly.TagMeta(name, sly.TagValueType.NONE if 2 <= i <= 5 else sly.TagValueType.ANY_STRING)
        for i, name in enumerate(tag_meta_names)
    ]
    project_meta = sly.ProjectMeta(tag_metas=tag_meta_list)
    api.project.update_meta(project.id, project_meta.to_json())

    dataset_path = "/mnt/c/users/german/documents/coffee-datasets/leaf/images"
    csv_file_path = os.path.join(os.path.dirname(dataset_path), "dataset.csv")
    annotations = read_dataset_tags(csv_file_path, tag_meta_list)

    dataset = api.dataset.create(project.id, "ds0", change_name_if_conflict=True)
    image_paths = [
        path
        for path in glob(os.path.join(dataset_path, "*"))
        if path.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    for batch in tqdm(sly.batched(image_paths), desc="Uploading images"):
        image_names = [sly.fs.get_file_name_with_ext(path) for path in batch]
        image_infos = api.image.upload_paths(dataset.id, image_names, batch)
        image_ids = [info.id for info in image_infos]
        annotations_batch = [create_annotation(path, annotations) for path in batch]
        api.annotation.upload_anns(image_ids, annotations_batch)

    return project

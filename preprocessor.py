import argparse
import os
import os.path
import yaml


def tag_title_to_tag_url_segment(tag):
    normalized_tag = tag.replace(
        " ", "-").lower().replace(".net", "-dot-net").replace(".", "-").replace("#", "-sharp").replace("++", "-plus-plus")
    if normalized_tag.startswith("-"):
        normalized_tag = normalized_tag[1:]
    return normalized_tag


class Creator:
    def __init__(self, config, args):
        self._config = config
        self._args = args

    def create_category_page(self, category, post_count):
        """
        Creates a category page.

        :param category: The URL segment of the category
        """
        fullpath = os.path.join("_category", category + ".md")
        if os.path.isfile(fullpath) and not self._args.overwrite:
            return

        # Get the category configuration
        try:
            category_config = self._config["categories"][category]
        except:
            category_config = {}

        # Create the category title
        try:
            title = category_config["title"]
        except:
            title = category.title().replace("-", " ")

        try:
            description = category_config["description"]
        except:
            description = ""

        with open(fullpath, "w", encoding="utf8") as f:
            f.write("---\n")
            f.write("layout: category\n")
            f.write(f"url_segment: {category}\n")
            f.write(f"title: {title}\n")
            f.write(f"post_count: {post_count}\n")
            for key in category_config.keys():
                if not key in ["title", "description"]:
                    f.write(f"{key}: {category_config[key]}\n")
            f.write("---\n\n")
            f.write(description)
            f.write("\n")

    def create_tag_page(self, tag, post_count):
        """
        Creates a tag page.

        :param tag: The human friendly name of the tag (i.e. not the URL segment)
        """
        normalized_tag = tag_title_to_tag_url_segment(tag)
        fullpath = os.path.join("_tag", normalized_tag + ".md")
        if os.path.isfile(fullpath) and not self._args.overwrite:
            return

        with open(fullpath, "w", encoding="utf8") as f:
            f.write("---\n")
            f.write("layout: tag\n")
            f.write(f"url_segment: {normalized_tag}\n")
            f.write(f"title: {tag}\n")
            f.write(f"post_count: {post_count}\n")
            f.write("---\n")


def extract_front_matter(fullpath):
    with open(fullpath, "r", encoding="utf8") as f:
        return next(yaml.safe_load_all(f))


class Collector:
    def __init__(self):
        self._categories = {}
        self._tags = {}

    def _add_category(self, category):
        if category in self._categories:
            self._categories[category] = self._categories[category] + 1
        else:
            self._categories[category] = 1

    def _add_tag(self, tag):
        if tag in self._tags:
            self._tags[tag] = self._tags[tag] + 1
        else:
            self._tags[tag] = 1

    def read_post(self, fullpath):
        front_matter = extract_front_matter(fullpath)
        categories = front_matter["categories"]
        for category in categories:
            self._add_category(category)
        tags = front_matter["tags"]
        for tag in tags:
            self._add_tag(tag)

    def get_categories(self):
        return self._categories

    def get_tags(self):
        return self._tags


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess category and tag pages")
    parser.add_argument(
        "--overwrite", help="Overwrite existing files", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    with open("_config.yml", "r", encoding="utf8") as f:
        config = yaml.safe_load(f)

    fullpaths = [
        os.path.join(root, p)
        for root, dirs, files in os.walk("_posts")
        for p in files
    ]

    collector = Collector()
    for post_fullpath in fullpaths:
        collector.read_post(post_fullpath)

    creator = Creator(config, args)
    for category, count in collector.get_categories().items():
        creator.create_category_page(category, count)
    for tag, count in collector.get_tags().items():
        creator.create_tag_page(tag, count)


if __name__ == "__main__":
    main()

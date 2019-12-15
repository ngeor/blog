import argparse
import os
import os.path
import yaml


def tag_title_to_tag_url_segment(tag):
    normalized_tag = tag.replace(
        " ", "-").lower().replace(".net", "-dot-net").replace(".", "-").replace("#", "-sharp").replace("++", "-plus-plus").replace("!", "")
    if normalized_tag.startswith("-"):
        normalized_tag = normalized_tag[1:]
    return normalized_tag


class PageInfo:
    """
    Information about a category or tag page.
    """

    def __init__(self, title, post_count):
        self.title = title
        self.post_count = post_count
        self.sort_index = f"{(9999 - post_count):04}-{title.lower()}"


class PageInfoCollection:
    """
    A collection of PageInfo instances.
    """

    def __init__(self):
        self._title_to_post_count = {}

    def add(self, title):
        if title in self._title_to_post_count:
            self._title_to_post_count[title] = self._title_to_post_count[title] + 1
        else:
            self._title_to_post_count[title] = 1

    def to_array(self):
        result = []
        for title, count in self._title_to_post_count.items():
            result.append(PageInfo(title, count))
        result.sort(key=lambda p: p.sort_index)
        return result


class Creator:
    """
    Creates category and tag pages.
    """

    def __init__(self, config, args):
        self._config = config
        self._args = args

    def create_category_page(self, category_page_info):
        """
        Creates a category page.

        :param category_page_info: A PageInfo instance of the category
        """
        category = category_page_info.title
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
            f.write(f"post_count: {category_page_info.post_count}\n")
            f.write(f"sort_index: {category_page_info.sort_index}\n")
            for key in category_config.keys():
                if not key in ["title", "description"]:
                    f.write(f"{key}: {category_config[key]}\n")
            f.write("---\n\n")
            f.write(description)
            f.write("\n")

    def create_tag_page(self, tag_page_info):
        """
        Creates a tag page.

        :param tag_page_info: A PageInfo of the tag. The title is the human friendly name of the tag (i.e. not the URL segment)
        """
        tag = tag_page_info.title
        normalized_tag = tag_title_to_tag_url_segment(tag)
        fullpath = os.path.join("_tag", normalized_tag + ".md")
        if os.path.isfile(fullpath) and not self._args.overwrite:
            return

        with open(fullpath, "w", encoding="utf8") as f:
            f.write("---\n")
            f.write("layout: tag\n")
            f.write(f"url_segment: {normalized_tag}\n")
            f.write(f"title: {tag}\n")
            f.write(f"post_count: {tag_page_info.post_count}\n")
            f.write(f"sort_index: {tag_page_info.sort_index}\n")
            f.write("---\n")


def extract_front_matter(fullpath):
    with open(fullpath, "r", encoding="utf8") as f:
        return next(yaml.safe_load_all(f))


class Collector:
    """
    Parses blog posts and collects category and tag information.
    """

    def __init__(self):
        self._categories = PageInfoCollection()
        self._tags = PageInfoCollection()

    def _add_category(self, category):
        self._categories.add(category)

    def _add_tag(self, tag):
        self._tags.add(tag)

    def read_post(self, fullpath):
        front_matter = extract_front_matter(fullpath)
        if "categories" in front_matter:
            categories = front_matter["categories"]
            for category in categories:
                self._add_category(category)
        else:
            print(f"No categories in {fullpath}")
        if "tags" in front_matter:
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
    for category_page_info in collector.get_categories().to_array():
        creator.create_category_page(category_page_info)
    for tag_page_info in collector.get_tags().to_array():
        creator.create_tag_page(tag_page_info)


if __name__ == "__main__":
    main()

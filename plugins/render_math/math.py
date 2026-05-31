"""Render Math: Math-rendering plugin for Pelican.

This plugin allows your site to render math. It uses
the MathJax JavaScript engine.

For Markdown, the plugin works by creating a Markdown
extension which is used during the Markdown compilation
stage. Math therefore gets treated like a "first class
citizen" in Pelican.

For ReStructuredText, the plugin instructs the reST engine
to output Mathjax for all math.

The MathJax script is by default automatically inserted
into the HTML.

Typogrify Compatibility
-----------------------
This plugin now plays nicely with Typogrify, but it
requires Typogrify version 2.0.7 or above.

User Settings
-------------
Users are also able to pass a dictionary of settings
in the settings file which will control how the MathJax
library renders things. This could be very useful for
template builders that want to adjust the look and feel of
the math. See README for more details.
"""

import functools
import os
import sys

from pelican import generators, signals

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from .pelican_mathjax_markdown_extension import PelicanMathJaxExtension
except ImportError:
    PelicanMathJaxExtension = None

try:
    string_type = basestring
except NameError:
    string_type = str


def process_settings(pelicanobj):
    """Set user-specified MathJax settings (see README for more details)."""
    mathjax_settings = {}

    # Default settings
    mathjax_settings["auto_insert"] = True
    mathjax_settings["align"] = "center"  # left, right, or center
    mathjax_settings["indent"] = "0em"
    mathjax_settings["process_escapes"] = "true"
    mathjax_settings["tex_extensions"] = ""  # MathJax 3 package names, e.g. ['color', 'physics']
    mathjax_settings["equation_numbering"] = "none"  # ams, all, or none
    mathjax_settings["process_summary"] = BeautifulSoup is not None

    # MathJax 3 CDN
    mathjax_settings["source"] = (
        "'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js'"
    )

    # Get the user-specified settings
    settings = pelicanobj.settings.get("MATH_JAX", None)

    if not isinstance(settings, dict):
        return mathjax_settings

    for key, value in ((key, settings[key]) for key in settings):
        if key == "align":
            if not isinstance(value, string_type):
                continue
            if value in ("left", "right", "center"):
                mathjax_settings[key] = value
            else:
                mathjax_settings[key] = "center"

        if key == "indent":
            mathjax_settings[key] = value

        if key == "source":
            mathjax_settings[key] = value

        if key == "auto_insert" and isinstance(value, bool):
            mathjax_settings[key] = value

        if key == "process_escapes" and isinstance(value, bool):
            mathjax_settings[key] = "true" if value else "false"

        if key == "process_summary" and isinstance(value, bool):
            if value and BeautifulSoup is None:
                print(
                    "BeautifulSoup4 is needed for summaries to be processed by render_math\nPlease install it"
                )
                value = False
            mathjax_settings[key] = value

        if key == "tex_extensions" and isinstance(value, list):
            # MathJax 3 package names: strip legacy .js suffix if present
            value = [v for v in value if isinstance(v, string_type)]
            value = [v[:-3] if v.endswith(".js") else v for v in value]
            mathjax_settings[key] = ", ".join("'%s'" % v for v in value)

        if key == "equation_numbering":
            # MathJax 3 uses lowercase: 'ams', 'all', 'none'
            if value is not None:
                mathjax_settings[key] = value.lower()
            else:
                mathjax_settings[key] = "none"

    return mathjax_settings


def process_summary(article):
    """Prevent summary truncation. Insert MathJax script so math will be rendered."""
    summary = article.summary
    summary_parsed = BeautifulSoup(summary, "html.parser")
    math = summary_parsed.find_all(class_="math")

    if len(math) > 0:
        last_math_text = math[-1].get_text()
        if len(last_math_text) > 3 and last_math_text[-3:] == "...":
            content_parsed = BeautifulSoup(article._content, "html.parser")
            full_text = content_parsed.find_all(class_="math")[len(math) - 1].get_text()
            math[-1].string = "%s ..." % full_text
            summary = summary_parsed.decode()

        if isinstance(article.get_summary, functools.partial):
            memoize_instance = article.get_summary.func.__self__
            memoize_instance.cache.clear()

        article.metadata["summary"] = (
            f"{summary}<script type='text/javascript'>{process_summary.mathjax_script}</script>"
        )


def configure_typogrify(pelicanobj, mathjax_settings):
    """Tell Typogrify to ignore math tags."""
    if not pelicanobj.settings.get("TYPOGRIFY", False):
        return

    try:
        from typogrify.filters import typogrify  # noqa: F401

        pelicanobj.settings["TYPOGRIFY_IGNORE_TAGS"].extend([".math", "script"])

    except (ImportError, TypeError) as e:
        pelicanobj.settings["TYPOGRIFY"] = False

        if isinstance(e, ImportError):
            print(
                "\nTypogrify is enabled but not installed; disabling.\n"
            )
        if isinstance(e, TypeError):
            print(
                "\nTypogrify >= 2.0.7 is required for render_math; disabling.\n"
            )


def process_mathjax_script(mathjax_settings):
    """Load the MathJax script template from file and render with the settings."""
    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/mathjax_script_template"
    ) as mathjax_script_template:
        mathjax_template = mathjax_script_template.read()

    return mathjax_template.format(**mathjax_settings)


def mathjax_for_markdown(pelicanobj, mathjax_script, mathjax_settings):
    """Instantiate customised Markdown extension to handle MathJax-related content."""
    config = {}
    config["mathjax_script"] = mathjax_script
    config["math_tag_class"] = "math"
    config["auto_insert"] = mathjax_settings["auto_insert"]

    try:
        if isinstance(pelicanobj.settings.get("MD_EXTENSIONS"), list):
            pelicanobj.settings["MD_EXTENSIONS"].append(PelicanMathJaxExtension(config))
        else:
            pelicanobj.settings["MARKDOWN"].setdefault("extensions", []).append(
                PelicanMathJaxExtension(config)
            )
    except:  # noqa: E722
        sys.excepthook(*sys.exc_info())
        sys.stderr.write(
            "\nError - the pelican mathjax markdown extension failed to configure. MathJax is non-functional.\n"
        )
        sys.stderr.flush()


def mathjax_for_rst(pelicanobj, mathjax_script, mathjax_settings):
    """Set up math for reStructuredText."""
    docutils_settings = pelicanobj.settings.get("DOCUTILS_SETTINGS", {})
    source_url = mathjax_settings["source"].strip("'\"")
    docutils_settings.setdefault("math_output", "MathJax %s" % source_url)
    pelicanobj.settings["DOCUTILS_SETTINGS"] = docutils_settings
    rst_add_mathjax.mathjax_script = mathjax_script


def pelican_init(pelicanobj):
    """Load the MathJax script and configure rendering for Markdown and RST."""
    mathjax_settings = process_settings(pelicanobj)
    mathjax_script = process_mathjax_script(mathjax_settings)

    configure_typogrify(pelicanobj, mathjax_settings)

    if PelicanMathJaxExtension:
        mathjax_for_markdown(pelicanobj, mathjax_script, mathjax_settings)

    mathjax_for_rst(pelicanobj, mathjax_script, mathjax_settings)

    process_summary.mathjax_script = None
    if mathjax_settings["process_summary"]:
        process_summary.mathjax_script = mathjax_script


def rst_add_mathjax(content):
    """Add MathJax script for reStructuredText."""
    _, ext = os.path.splitext(os.path.basename(content.source_path))
    if ext != ".rst":
        return

    if 'class="math"' in content._content:
        content._content += (
            "<script type='text/javascript'>%s</script>"
            % rst_add_mathjax.mathjax_script
        )


def process_rst_and_summaries(content_generators):
    """Apply MathJax to RST content and fix truncated summaries."""
    for generator in content_generators:
        if isinstance(generator, generators.ArticlesGenerator):
            for article in (
                generator.articles + generator.translations + generator.drafts
            ):
                rst_add_mathjax(article)
                if process_summary.mathjax_script is not None:
                    process_summary(article)
        elif isinstance(generator, generators.PagesGenerator):
            for page in generator.pages:
                rst_add_mathjax(page)
            for page in generator.hidden_pages:
                rst_add_mathjax(page)


def register():
    """Register the plugin."""
    signals.initialized.connect(pelican_init)
    signals.all_generators_finalized.connect(process_rst_and_summaries)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# standard object to wrap file and access easily to the filename
#
###############################################################################

import re
import copy
import mistune
from stringcase import snakecase, camelcase
import pymdtools.common as common

###############################################################################
# re expression used for comment
###############################################################################
__comment_re__ = \
    r"<!--(?P<comment>[\s\S]*?)-->"

###############################################################################
# re expression used for instruction
###############################################################################
__instruction_re__ = r"(?P<name>[a-zA-Z0-9_-]+)\s*[:=]\s*(?P<value>.*)"

###############################################################################
# get new identifier for the nash standalone form
#
# @param label a string for inspiration
# @return An id
###############################################################################
@common.static(__id_counter__=None)
def get_new_id(label=None):
    if get_new_id.__id_counter__ is None:
        get_new_id.__id_counter__ = 0

    get_new_id.__id_counter__ += 1

    result = label

    if result is None:
        result = "id"

    result = camelcase(snakecase(result))
    result = result.replace("_", "")
    result = "id%s%04d" % (result[:10], get_new_id.__id_counter__)

    return result

###############################################################################
# strip XML comment.
# Remove all xml comment from a text
#
# @param text the markdown text
# @return the text without xml comment
###############################################################################
def strip_xml_comment(text):
    result = re.sub(__comment_re__, "", text)

    return result

###############################################################################
# get comment from text.
#
# @param text the markdown text
# @return the lines
###############################################################################
def read_instructions(text):
    result = {}
    comments = re.finditer(__comment_re__, text)
    for comment in comments:
        line = comment.group('comment').strip()
        match = re.search(__instruction_re__, line)
        if match is not None:
            result[match.group('name').lower()] = match.group('value')

    return result

###############################################################################
# get comment from text.
#
# @param text the markdown text
# @return the lines
###############################################################################
def get_render_couple(template, context):
    context['begin'] = ''
    begin = template.render(context)

    del context['begin']
    context['end'] = ''
    end = template.render(context)

    return (begin, end)


###############################################################################
# Render generator
###############################################################################
class RendererGenerator:

    ###########################################################################
    # the dict generator
    ###########################################################################
    __generator = {}

    ###########################################################################
    # test a name
    #
    # @param name the name of the generator
    # @param result of the test
    ###########################################################################
    @staticmethod
    def is_renderer(name):
        return name.lower() in RendererGenerator.__generator

    ###########################################################################
    # register a new generator
    #
    # @param name the name of the generator
    # @param creator the function to create the renderer
    ###########################################################################
    @staticmethod
    def register(name, creator):
        RendererGenerator.__generator[name.lower()] = creator
        return True

    ###########################################################################
    # generate a renderer
    #
    # @param name the name of the generator
    # @return the renderer
    ###########################################################################
    @staticmethod
    def create(name, **kwargs):
        return RendererGenerator.__generator[name.lower()](**kwargs)


###############################################################################
# An object to manage the context of a page
###############################################################################
class ContextManagment:
    ###########################################################################
    # initialisation with the context
    #
    # @param the context
    ###########################################################################
    def __init__(self, context):
        self.__context = context
        self.__init_instructions = {}
        self.__instructions = {}

    ###########################################################################
    # the instrcution environment
    # @return the value
    ###########################################################################
    @property
    def init_instructions(self):
        return self.__init_instructions

    ###########################################################################
    # the instrcution environment
    # @param value The value to set
    ###########################################################################
    @init_instructions.setter
    def init_instructions(self, value):
        self.__init_instructions = value

    ###########################################################################
    # the instrcution environment
    # @return the value
    ###########################################################################
    @property
    def instructions(self):
        return self.__instructions

    ###########################################################################
    # the instrcution environment
    # @param value The value to set
    ###########################################################################
    @instructions.setter
    def instructions(self, value):
        self.__instructions = value

    ###########################################################################
    # empty the instructions list
    ###########################################################################
    def del_instructions(self):
        self.__instructions = {}

    ###########################################################################
    # Build the complet context with instruction
    ###########################################################################
    @property
    def context(self):
        result = copy.deepcopy(self.__context)
        for key in self.__init_instructions:
            result[key] = copy.deepcopy(self.__init_instructions[key])
        for key in self.__instructions:
            result[key] = copy.deepcopy(self.__instructions[key])

        return result

###############################################################################
# An object to wrap the mistune render
###############################################################################
class JinjaEnvManagment:
    def __init__(self, jinja_env):
        self.__jinja_env = jinja_env

    @property
    def jinja_env(self):
        return self.__jinja_env


###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererDefault(JinjaEnvManagment):

    ###########################################################################
    # generate a renderer
    #
    # @return the renderer
    ###########################################################################
    @staticmethod
    def generate(**kwargs):
        return RendererDefault(jinja_env=kwargs['jinja_env'])

    ###########################################################################
    # register the renderer
    ###########################################################################
    __register = RendererGenerator.register('default', generate.__func__)

    ###########################################################################
    ###########################################################################
    def __init__(self, jinja_env):
        JinjaEnvManagment.__init__(self, jinja_env)

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        if level == 1:
            return self.header_1(text)

        begin = '<h%d>%s</h%d>\n' % (level, text, level)
        end = ''
        return (begin, end)

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header_1(self, text):
        begin = self.jinja_env.get_template("header_1.j2").render(
            {"begin": '', 'text': text})
        end = self.jinja_env.get_template("header_1.j2").render(
            {"end": '', 'text': text})
        return (begin, end)


###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererCallapsable(RendererDefault, ContextManagment):

    ###########################################################################
    # generate a renderer
    #
    # @return the renderer
    ###########################################################################
    @staticmethod
    def generate(**kwargs):
        return RendererCallapsable(jinja_env=kwargs['jinja_env'],
                                   context=kwargs['context'])

    ###########################################################################
    # register the renderer
    ###########################################################################
    __register = RendererGenerator.register('collapsable', generate.__func__)

    ###########################################################################
    # init the callapsable
    ###########################################################################
    def __init__(self, jinja_env, context):
        RendererDefault.__init__(self, jinja_env)
        ContextManagment.__init__(self, context)

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        self.instructions = read_instructions(text)
        text = strip_xml_comment(text)
        context = self.context

        if ('collapsable' not in context) or \
                (context['collapsable'] == "off"):
            self.del_instructions()
            return RendererDefault.header(self, text, level, raw=raw)

        if level == 1:
            return self.header_1(text)

        context['level'] = level
        context['text'] = text
        context['fresh_uid'] = get_new_id(text)

        (begin, end) = get_render_couple(
            self.jinja_env.get_template("header_n.j2"), context)

        self.del_instructions()
        return (begin, end)


###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererLink(ContextManagment, JinjaEnvManagment):

    ###########################################################################
    # init the link renderer
    ###########################################################################
    def __init__(self, jinja_env, context, default_link="normal"):
        JinjaEnvManagment.__init__(self, jinja_env)
        ContextManagment.__init__(self, context)
        self.__default_link = default_link

    ###########################################################################
    # Rendering a given link with content and title.
    #
    # @param link: href link for ``<a>`` tag.
    # @param title: title content for `title` attribute.
    # @param text: text content for description.
    ###########################################################################
    def link(self, link, title, text):
        self.instructions = read_instructions(text)
        text = strip_xml_comment(text)
        context = self.context
        context['link'] = {'url': mistune.escape_link(link), 'name': text}

        if title is not None:
            context['link']['title'] = title

        if 'normal-link' in context:
            return self.jinja_env.get_template(
                "link_normal.j2").render(context)

        link_model = self.__default_link

        if 'link-model' in context:
            link_model = context['link-model']

        return self.jinja_env.get_template(
            "link_" + link_model + ".j2").render(context)


###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererSectionBanner(RendererLink):

    ###########################################################################
    # generate a renderer
    #
    # @return the renderer
    ###########################################################################
    @staticmethod
    def generator(template):
        def generate(**kwargs):
            return RendererSectionBanner(**kwargs, template=template)
        return generate

    ###########################################################################
    # register the renderer
    ###########################################################################
    __register = \
        RendererGenerator.register('section-banner',
                                   generator.__func__("banner")) and \
        RendererGenerator.register('section:banner',
                                   generator.__func__("banner")) and \
        RendererGenerator.register('section-stories',
                                   generator.__func__("stories")) and \
        RendererGenerator.register('section:stories',
                                   generator.__func__("stories")) and \
        RendererGenerator.register('section-courses',
                                   generator.__func__("courses")) and \
        RendererGenerator.register('section:courses',
                                   generator.__func__("courses"))

    ###########################################################################
    # init the callapsable
    ###########################################################################
    def __init__(self, jinja_env, context,
                 init_param=None,
                 template="banner"):

        default_link_conf = {}
        default_link_conf['banner'] = "box"
        default_link_conf['stories'] = "box-trans"
        default_link_conf['courses'] = "normal"

        RendererLink.__init__(self,
                              jinja_env=jinja_env,
                              context=context,
                              default_link=default_link_conf[template])

        if init_param is not None:
            self.init_instructions = {'image': init_param}

        self.__template = template

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        self.instructions = read_instructions(text)
        text = strip_xml_comment(text)
        context = self.context

        if level != 1:
            self.del_instructions()
            return ('<h%d>%s</h%d>\n' % (level, text, level), '')

        context['text'] = text
        context['fresh_uid'] = get_new_id(text)

        (begin, end) = get_render_couple(
            self.jinja_env.get_template("section_" + self.__template + ".j2"),
            context)

        self.del_instructions()
        return (begin, end)

###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererSectionInformation(RendererLink):

    ###########################################################################
    # generate a renderer
    #
    # @return the renderer
    ###########################################################################
    @staticmethod
    def generate(**kwargs):
        return RendererSectionInformation(**kwargs)

    ###########################################################################
    # register the renderer
    ###########################################################################
    __register = \
        RendererGenerator.register(
            'section-information', generate.__func__) and \
        RendererGenerator.register(
            'section:information', generate.__func__)

    ###########################################################################
    # init the callapsable
    ###########################################################################
    def __init__(self, jinja_env, context,
                 init_param=None):
        RendererLink.__init__(self,
                              jinja_env=jinja_env,
                              context=context,
                              default_link="normal")

        if init_param is not None:
            self.init_instructions = {'offset': init_param}

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        self.instructions = read_instructions(text)
        text = strip_xml_comment(text)
        context = self.context

        if level != 1:
            self.del_instructions()
            return ('<li><h3>%s</h3>\n' % (text), '</li>')

        context['fresh_uid'] = get_new_id(text)

        (begin, end) = get_render_couple(
            self.jinja_env.get_template("section_information.j2"), context)

        self.del_instructions()
        return (begin, end)

###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererSectionWelcome(RendererLink):

    ###########################################################################
    # generate a renderer
    #
    # @return the renderer
    ###########################################################################
    @staticmethod
    def generate(**kwargs):
        return RendererSectionWelcome(jinja_env=kwargs['jinja_env'],
                                      context=kwargs['context'])

    ###########################################################################
    # register the renderer
    ###########################################################################
    __register = \
        RendererGenerator.register('section-welcome', generate.__func__) and \
        RendererGenerator.register('section:welcome', generate.__func__)

    ###########################################################################
    # init the callapsable
    ###########################################################################
    def __init__(self, jinja_env, context):
        RendererLink.__init__(self,
                              jinja_env=jinja_env,
                              context=context,
                              default_link="normal")
        self.__h3_is_open = False

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        self.instructions = read_instructions(text)
        text = strip_xml_comment(text)
        context = self.context
        context['text'] = text
        context['fresh_uid'] = get_new_id(text)

        if level != 1:
            extra_row = ""
            if not self.__h3_is_open:
                extra_row += '</div><div class="row">'
                self.__h3_is_open = True

            if text.replace(' ', '').isdigit():
                context['number'] = ''

            if 'image_text' not in context:
                context['image_text'] = re.sub(r'<.*?>', '', text).strip()

            (begin, end) = get_render_couple(
                self.jinja_env.get_template("section_colmd3.j2"), context)

            self.del_instructions()
            return (extra_row + begin, end)

        (begin, end) = get_render_couple(
            self.jinja_env.get_template("section_welcome.j2"), context)

        self.del_instructions()
        return (begin, end)


###############################################################################
# An object to wrap the mistune render
###############################################################################
class RendererDispatch(mistune.Renderer):

    def __init__(self, **kwargs):
        mistune.Renderer.__init__(self, **kwargs)
        self.__current_level = 0
        self.__renderers = {}
        self.__renderers[0] = RendererGenerator.create('default', **kwargs)
        self.__end_stack = {}
        self.__kwargs = kwargs

    ###########################################################################
    # Get renderer
    ###########################################################################
    def get_renderer(self, level=None):
        local_level = level
        if level is None:
            local_level = self.level

        while (local_level not in self.__renderers) and (local_level > 0):
            local_level = local_level - 1
        return self.__renderers[local_level]

    ###########################################################################
    # Get a function from the renderer
    ###########################################################################
    def get_renderer_method(self, method, level=None):
        if level is None:
            level = self.level
        renderer = self.get_renderer(level)
        if hasattr(renderer, method) and callable(getattr(renderer, method)):
            return getattr(renderer, method)
        return None

    ###########################################################################
    # Get the level of header
    # @return the current level
    ###########################################################################
    @property
    def level(self):
        return self.__current_level

    ###########################################################################
    # set the new level
    # @param value The value to set
    ###########################################################################
    def add_to_stack(self, level, content):
        if level in self.__end_stack:
            raise 'should empty the tsak'

        self.__end_stack[level] = content

    ###########################################################################
    # set the new level
    # @param value The value to set
    ###########################################################################
    def change_level(self, new_level):
        result = ''

        if new_level < 0:
            new_level = 0

        for level in list(reversed(range(new_level,
                                         self.__current_level + 1))):
            if level in self.__end_stack:
                result += self.__end_stack[level]
                del self.__end_stack[level]
            if level in self.__renderers:
                del self.__renderers[level]

        self.__current_level = new_level

        return result

    ###########################################################################
    # Change the renderer if needed
    # @param text the text containing instrction
    ###########################################################################
    def change_renderer_on_instrcution(self, text):
        # Find the new renderer if needed
        instructions = read_instructions(text)

        new_renderer = None
        for key in instructions:
            candidats = [(key, instructions[key]),
                         (key + ":" + instructions[key], None)]
            for candidat in candidats:
                if RendererGenerator.is_renderer(candidat[0]):
                    if new_renderer is None:
                        new_renderer = candidat
                    else:
                        raise Exception("Find two renderers")

        if new_renderer is not None:
            self.__renderers[self.level] = \
                RendererGenerator.create(new_renderer[0],
                                         init_param=new_renderer[1],
                                         **self.__kwargs)

    ###########################################################################
    # set the new level
    # @param value The value to set
    ###########################################################################
    def close(self):
        return self.change_level(0)

    ###########################################################################
    # Rendering header/heading tags like ``<h1>`` ``<h2>``.
    #
    # @param text: rendered text content for the header.
    # @param level: a number for the header level, for example: 1.
    # @param raw: raw text content of the header.
    ###########################################################################
    def header(self, text, level, raw=None):
        # change the level and get the end of the previous
        unstack = self.change_level(level)

        # change the renderer if needed
        self.change_renderer_on_instrcution(text)

        # finally do the job with the renderer
        method = self.get_renderer_method('header')
        if method is None:
            return mistune.Renderer.header(self, text, level, raw=raw)

        (begin, end) = method(text, level, raw=raw)

        self.add_to_stack(level, end)

        return unstack + begin

    ###########################################################################
    # Returns the default, empty output value for the renderer.
    #
    # All renderer methods use the '+=' operator to append to this value.
    # Default is a string so rendering HTML can build up a result string with
    # the rendered Markdown.
    #
    # Can be overridden by Renderer subclasses to be types like an empty
    # list, allowing the renderer to create a tree-like structure to
    # represent the document (which can then be reprocessed later into a
    # separate format like docx or pdf).
    ###########################################################################
    def placeholder(self):
        return mistune.Renderer.placeholder(self)

    ###########################################################################
    # Rendering block level code. ``pre > code``.
    #
    # @param code: text content of the code block.
    # @param lang: language of the given code.
    ###########################################################################
    def block_code(self, code, lang=None):
        return mistune.Renderer.block_code(self, lang, code)

    ###########################################################################
    # Rendering <blockquote> with the given text.
    #
    # @param text: text content of the blockquote.
    ###########################################################################
    def block_quote(self, text):
        return mistune.Renderer.block_quote(self, text)

    ###########################################################################
    # Rendering block level pure html content.
    #
    # @param html: text content of the html snippet.
    ###########################################################################
    def block_html(self, html):
        return mistune.Renderer.block_html(self, html)

    ###########################################################################
    # Rendering method for ``<hr>`` tag.
    ###########################################################################
    def hrule(self):
        return mistune.Renderer.hrule(self)

    ###########################################################################
    # Rendering list tags like ``<ul>`` and ``<ol>``.
    #
    # @param body: body contents of the list.
    # @param ordered: whether this list is ordered or not.
    ###########################################################################
    def list(self, body, ordered=True):
        return mistune.Renderer.list(self, body, ordered=ordered)

    ###########################################################################
    # Rendering list item snippet. Like ``<li>``.
    ###########################################################################
    def list_item(self, text):
        return mistune.Renderer.list_item(self, text)

    ###########################################################################
    # Rendering paragraph tags. Like ``<p>``.
    ###########################################################################
    def paragraph(self, text):
        return mistune.Renderer.paragraph(self, text)

    ###########################################################################
    # Rendering table element. Wrap header and body in it.
    #
    # @param header: header part of the table.
    # @param body: body part of the table.
    ###########################################################################
    def table(self, header, body):
        return mistune.Renderer.table(self, header, body)

    ###########################################################################
    # Rendering a table row. Like ``<tr>``.
    #
    # @param content: content of current table row.
    ###########################################################################
    def table_row(self, content):
        return mistune.Renderer.table_row(self, content)

    ###########################################################################
    # Rendering a table cell. Like ``<th>`` ``<td>``.
    #
    # @param content: content of current table cell.
    # @param header: whether this is header or not.
    # @param align: align of current table cell.
    ###########################################################################
    def table_cell(self, content, **flags):
        return mistune.Renderer.table_cell(self, content, **flags)

    ###########################################################################
    # Rendering **strong** text.
    #
    # @param text: text content for emphasis.
    ###########################################################################
    def double_emphasis(self, text):
        return mistune.Renderer.double_emphasis(self, text)

    ###########################################################################
    # Rendering *emphasis* text.
    #
    # @param text: text content for emphasis.
    ###########################################################################
    def emphasis(self, text):
        return mistune.Renderer.emphasis(self, text)

    ###########################################################################
    # Rendering inline `code` text.
    #
    # @param text: text content for inline code.
    ###########################################################################
    def codespan(self, text):
        return mistune.Renderer.codespan(self, text)

    ###########################################################################
    # Rendering line break like ``<br>``.
    ###########################################################################
    def linebreak(self):
        return mistune.Renderer.linebreak(self)

    ###########################################################################
    # Rendering ~~strikethrough~~ text.
    #
    # @param text: text content for strikethrough.
    ###########################################################################
    def strikethrough(self, text):
        return mistune.Renderer.strikethrough(self, text)

    ###########################################################################
    # Rendering unformatted text.
    #
    # @param text: text content.
    ###########################################################################
    def text(self, text):
        return mistune.Renderer.text(self, text)

    ###########################################################################
    # Rendering escape sequence.
    #
    # @param text: text content.
    ###########################################################################
    def escape(self, text):
        return mistune.Renderer.escape(self, text)

    ###########################################################################
    # Rendering a given link or email address.
    #
    # @param link: link content or email address.
    # @param is_email: whether this is an email or not.
    ###########################################################################
    def autolink(self, link, is_email=False):
        return mistune.Renderer.autolink(self, link, is_email=is_email)

    ###########################################################################
    # Rendering a given link with content and title.
    #
    # @param link: href link for ``<a>`` tag.
    # @param title: title content for `title` attribute.
    # @param text: text content for description.
    ###########################################################################
    def link(self, link, title, text):
        method = self.get_renderer_method('link')
        if method is None:
            return mistune.Renderer.link(self, link, title, text)
        return method(link, title, text)

    ###########################################################################
    # Rendering a image with title and text.
    #
    # @param src: source link of the image.
    # @param title: title text of the image.
    # @param text: alt text of the image.
    ###########################################################################
    def image(self, src, title, text):
        method = self.get_renderer_method('image')
        if method is None:
            return mistune.Renderer.image(self, src, title, text)
        return method(src, title, text)

    ###########################################################################
    # Rendering span level pure html content.
    #
    # @param html: text content of the html snippet.
    ###########################################################################
    def inline_html(self, html):
        return mistune.Renderer.inline_html(self, html)

    ###########################################################################
    # Rendering newline element.
    ###########################################################################
    def newline(self):
        return mistune.Renderer.newline(self)

    ###########################################################################
    # Rendering the ref anchor of a footnote.
    #
    # @param key: identity key for the footnote.
    # @param index: the index count of current footnote.
    ###########################################################################
    def footnote_ref(self, key, index):
        return mistune.Renderer.footnote_ref(self, key, index)

    ###########################################################################
    # Rendering a footnote item.
    #
    # @param key: identity key for the footnote.
    # @param text: text content of the footnote.
    ###########################################################################
    def footnote_item(self, key, text):
        return mistune.Renderer.footnote_item(self, key, text)

    ###########################################################################
    # Wrapper for all footnotes.
    #
    # @param text: contents of all footnotes.
    ###########################################################################
    def footnotes(self, text):
        return mistune.Renderer.footnotes(self, text)

# TODO: autocomment generator for closing curlies
# TODO: Figure out how to handle nested arrays
# TODO: understand class structure better, there's def some vars that could be shared
# TODO: look at this https://bitbucket.org/blackaura/pyparsephp
# TODO: look at this https://github.com/ramen/phply
# TODO: get proper line endings
# TODO: line up ternary statements
import sublime
import sublime_plugin
# import re


class VanityPhpCommand(sublime_plugin.TextCommand):

    SETTINGS_GROUP_SUBLIME = 'Sublime'
    SETTINGS_GROUP_PHPVANITY = 'PhpVanity'

    control_tokens = ['if', 'for', 'foreach', 'switch']

    comment_tokens = ['//', '#', '/*', '*/']

    def run(self, edit, **kwargs):

        print 'vanity'
        print self.line_ending()

        action = kwargs.get('action', None)

        if action == 'control_statements':
            self.control_statements(edit)
        if action == 'control_spacing':
            self.control_spacing(edit)
        elif action == 'single_line_curlies':
            self.single_line_curlies(edit)
        elif action == 'array_format':
            self.array_format(edit)
        else:
            print "Vanity doesn't know what to do."

    # TODO: Check for the presence of the alignment plugin
    # TODO: handle the situation where there's a array element on the same line as the array keyword
    def array_format(self, edit):
        print "array_format"

        sels = self.view.sel()

        for sel in sels:

            region = self.view.line(sel)

            array_region = self.find_array_region(region)

            array_lines = self.view.lines(array_region)
            declaration = self.view.substr(array_lines[0])

            # Figure out how much whitespace is in front of the declaration
            whitespace = self.leading_whitespace(declaration)

            # Check if there's valid indentation
            # TODO: show the user something, cuz this is bad.
            # if (whitespace / 2) != 1:
            #     print "we have some bad indentation here"

            desired_indent = whitespace + self.setting(self.SETTINGS_GROUP_PHPVANITY, 'array_indent')

            # iterate through the lines, and indent accordingly
            # TODO: ignore nested arrays
            opening = ''
            items = ''
            closing = ''
            for idx, val in enumerate(array_lines):

                line = self.view.substr(val)

                # Skip the declaration, as it's the only line correctly indented
                if idx == 0:

                    # properly format array openings
                    opening = line.replace('array (', 'array(') + "\n"
                    continue

                # make the closing match the opening
                if idx == (len(array_lines) - 1):
                    line = line.lstrip().rstrip()
                    line = line.rjust(len(line)+whitespace, ' ')
                    closing = line
                    continue

                # strip whitespace from left hand side, and add it back
                line = line.lstrip().rstrip()
                line = line.rjust(len(line)+desired_indent, ' ')

                items += line + "\n"

            self.view.replace(edit, array_region, opening + items + closing)

            # Get the modified region
            modified_region = self.find_array_region(array_region)

            # remove the opening and closing lines
            modified_lines = self.view.lines(modified_region)
            modified_lines.pop()
            del modified_lines[0]

            self.view.run_command("alignment", {'begin': modified_lines[0].begin(), 'end': modified_lines[-1].end()})

    # Need to find where the array( bit is declared
    # TODO: look for nested arrays, by
    # TODO: start in the middle of the selection, as someone could've selected more
    def find_array_region(self, region):
        print "find_array_region"

        line_above = self.view.line(region.begin())
        line_below = self.view.line(region.end())

        opening = False
        while opening is False:
            if self.view.substr(line_above).find('array') != -1:
                opening = line_above
                break
            elif line_above.begin() - 1 < 0:
                print "out of bounds on top"
                break
            else:
                line_above = self.view.line(line_above.begin() - 1)

        closing = False
        while closing is False:
            if self.view.substr(line_below).find(');') != -1:
                closing = line_below
                break
            elif line_below.end() + 1 > self.view.size():
                print "out of bounds on bottom"
                break
            else:
                line_below = self.view.line(line_below.end() + 1)

        if opening is not False and closing is not False:
            return sublime.Region(line_above.begin(), line_below.end())
        else:
            return False

    def control_statements(self, edit):
        print "control_statements"

        sels = self.view.sel()
        for sel in sels:

            lines_sel = self.view.line(sel)
            code = self.view.substr(lines_sel)
            codeLinesRaw = code.splitlines()

            # TODO: expand this to switches, elses, etc, and also manage
            #   spacing between curlies, same as parens
            brace = '('

            # Check it's only 2 lines
            if len(codeLinesRaw) != 1:
                print "Wrong # of lines"
                return()

            # Check there are no comments in our selection
            for comment in self.comment_tokens:
                if code.find(comment) != -1:
                    print "There's some comments in here"
                    return

            # Check that there's a control statement we know
            controlWord = False
            for controlWord_ in self.control_tokens:
                if codeLinesRaw[0].find(controlWord_) != -1:
                    controlWord = controlWord_
                    break

            if controlWord is False:
                print "No controlWord"
                return()

            # space the control word from the parens
            s = controlWord + brace
            r = controlWord + ' ' + brace
            replacement = code.replace(s, r, 1)
            replacement = replacement.replace('){', ') {', 1)

            # TODO: space the inside of the parens, too.

            # replace and we're done
            self.view.replace(edit, lines_sel, replacement)

    def single_line_curlies(self, edit):
        print "single_line_curlies"

        sels = self.view.sel()
        for sel in sels:

            lines_sel = self.view.line(sel)
            code = self.view.substr(lines_sel)
            codeLinesRaw = code.splitlines()

            # Check it's only 2 lines
            if len(codeLinesRaw) != 2:
                print "Wrong # of lines"
                return()

            # Check there are no comments in either line
            for comment in self.comment_tokens:
                if code.find(comment) != -1:
                    print "There's some comments in here"
                    return

            # Check that there's control structure
            controlWord = False
            for controlWord_ in self.control_tokens:
                if codeLinesRaw[0].find(controlWord_) != -1:
                    controlWord = controlWord_
                    break

            if controlWord is False:
                print "No controlWord"
                return()

            # figure out how how much whitespace was in front of the control char
            controlPos = codeLinesRaw[0].find(controlWord)

            # Look if there are curlies
            curlies = False
            if code.find('{') != -1:
                curlies = True

            if curlies is True:
                print "found curlies"
                return

            # Trim any whitespace off the end of the line, and
            # add the curly to the first line
            controlLine = codeLinesRaw[0].rstrip() + " {\n"

            # Add an additional line with the closing curly
            closingCurly = "\n" + "}".rjust(controlPos+1)

            # replace and we're done
            self.view.replace(edit, lines_sel, controlLine + codeLinesRaw[1] + closingCurly)

    # TODO: Make sure there's only one lines
    def control_spacing(self, edit):
        print "control_spacing"

        sels = self.view.sel()
        for sel in sels:

            lines_sel = self.view.line(sel)
            replacement = self.view.substr(lines_sel)

            # self.fix_paren_spacing(replacement)
            # return()

            # Find the position of the first / opening paren
            open_pos = replacement.find('(')

            # Check the next char is whitespace
            if replacement[open_pos+1] != ' ':
                replacement = replacement.replace('(', '( ', 1)

            # count # of opening + closing parens on the line.
            num_open_parens = replacement.count('(')
            num_close_parens = replacement.count(')')

            if num_close_parens != num_open_parens:
                print "No closing on this line"
            else:
                if replacement[open_pos-1] != ' ':
                    replacement = self.rreplace(replacement, ')', ' )', 1)

            self.view.replace(edit, lines_sel, replacement)

    def fix_paren_spacing(edit, s):

        for paren in [('(', '( ', 'add'), (')', ' )', 'sub')]:

            offset = 0

            # print '|'+paren[0]+'|'
            # print '|'+paren[1]+'|'
            # print '|'+paren[2]+'|'

            pos = s.find(paren[0], offset)

            print pos

            while pos != -1:

                print s

                if paren[2] == 'add':
                    start_end = pos
                elif paren[2] == 'sub':
                    start_end = pos

                if paren[2] == 'add':
                    end_start = pos+1
                elif paren[2] == 'sub':
                    end_start = pos + 1

                start = s[0:start_end]
                end = s[end_start:len(s)]

                print start
                print end

                s = start + paren[1] + end

                print s

                if paren[2] == 'add':
                    offset = pos+1
                elif paren[2] == 'sub':
                    offset = pos+2

                pos = s.find(paren[0], offset)

    # TODO: probably need a better way to do this
    def leading_whitespace(edit, s):
        whitespace = 0
        for c in s:
            if c == ' ':
                whitespace += 1
            else:
                break

        return whitespace

    def rreplace(edit, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def setting(self, group, setting):

        if group == 'Sublime':
            settings = self.view.settings()
        elif group == 'PhpVanity':
            settings = sublime.load_settings("Default.sublime-settings")

        return settings.get(setting)

    def line_ending(self):

        ending = self.setting(self.SETTINGS_GROUP_SUBLIME, 'default_line_ending')

        if ending == 'unix':
            return "\n"
        elif ending == 'windows':
            return "\r\n"

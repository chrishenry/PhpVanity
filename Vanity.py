# TODO: function for correctly spacing arrays
# TODO: autocomment generator for closing curlies
# TODO: array formatter to add 2 soft tabs
# TODO: Improve upon current =s liner upper
import sublime
import sublime_plugin


class VanityPhpCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):

        print 'vanity'

        action = kwargs.get('action', None)

        if action == 'control_statements':
            self.control_statements(edit)
        elif action == 'single_line_curlies':
            self.single_line_curlies(edit)
        elif action == 'array_format':
            self.array_format(edit)
        else:
            print "Vanity doesn't know what to do."

    def array_format(self, edit):
        sels = self.view.sel()
        for sel in sels:

            region = self.view.line(sel)
            lines = self.view.lines(region)

            # Check it's there's more than one line
            if len(lines) <= 1:
                print "Wrong # of lines"
                return()

            # find if there's an array declaration in the selection,
            #   and what line it's on
            found_line = False
            for line in lines:
                if self.view.substr(line).find('array(') > 0:
                    found_line = line

            if found_line is False:
                array_region = self.find_array_region(region)
            else:
                print self.view.substr(found_line)

            full_array = self.view.substr(array_region)

            print full_array

    # Need to find where the array( bit is declared
    def find_array_region(self, region):
        beginning = region.begin()
        end = region.end()

        line_above = self.view.line(beginning-1)
        line_below = self.view.line(end+1)

        opening = False
        while opening is False:
            if self.view.substr(line_above).find('array(') != -1:
                opening = line_above
            elif line_above.begin() - 1 < 0:
                print "out of bounds on top"
                break
            else:
                line_above = self.view.line(line_above.begin() - 1)

        closing = False
        while closing is False:
            if self.view.substr(line_below).find(');') != -1:
                closing = line_below
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
        sels = self.view.sel()
        for sel in sels:

            lines_sel = self.view.line(sel)
            code = self.view.substr(lines_sel)
            codeLinesRaw = code.splitlines()

            # TODO: expand this to switches, elses, etc, and also manage
            #   spacing between curlies, same as parens
            controlWords = ['if', 'for', 'foreach']
            brace = '('

            # Check it's only 2 lines
            if len(codeLinesRaw) != 1:
                print "Wrong # of lines"
                return()

            # Check there are no comments in our selection
            comments = ['//', '#', '/*', '*/']
            for comment in comments:
                if code.find(comment) != -1:
                    print "There's some comments in here"
                    return

            # Check that there's a control statement we know
            controlWord = False
            for controlWord_ in controlWords:
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
        sels = self.view.sel()
        for sel in sels:

            print "SingleLineCurliesCommand"

            lines_sel = self.view.line(sel)
            code = self.view.substr(lines_sel)
            codeLinesRaw = code.splitlines()

            controlWords = ['if', 'for', 'foreach']

            # Check it's only 2 lines
            if len(codeLinesRaw) != 2:
                print "Wrong # of lines"
                return()

            # Check there are no comments in either line
            comments = ['//', '#', '/*', '*/']
            for comment in comments:
                if code.find(comment) != -1:
                    print "There's some comments in here"
                    return

            # Check that there's control structure
            controlWord = False
            for controlWord_ in controlWords:
                if codeLinesRaw[0].find(controlWord_) != -1:
                    controlWord = controlWord_
                    break

            print controlWord

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

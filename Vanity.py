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
        else:
            print "Vanity doesn't know what to do."

    def control_statements(self, edit):
        sels = self.view.sel()
        for sel in sels:

            print "ControlStatementSpacingCommand"

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

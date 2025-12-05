import re
import stdlib.__entry__ as stdlib
cComment = re.compile(r"^\/\/(.+)")
cComment2 = re.compile(r"(.+)\s*\/\/(.+)")
cInclude = re.compile(r"^\#include\s*\<(.+)\>\s*")
shortCutImport = re.compile(r"^use\s+(.+)\s*")
shortCutImportAs = re.compile(r"^use\s+(.+)\s+as\s+(.+)\s*")
shortCutImportFrom = re.compile(r"^use\s+([A-Za-z_][A-Za-z0-9_]*)\.\{([^}]+)\}\s*$")
whenStatement = re.compile(r"^when\s+(.+):$")

inString = False
def pyxify_parse(string):
    global inString
    overall = ""
    pieces = string.splitlines() if string else []

    currentLine = 0
    for peice in pieces:
        index = 0
        length = len(peice)

        while index < length:
            nxt  = peice[index+1] if index+1 < length else ""
            nxt2 = peice[index+2] if index+2 < length else ""

            if peice[index] == "'" and nxt == "'" and nxt2 == "'":
                inString = not inString
                index += 3
                continue

            elif cComment.match(peice) and not inString:
                break
            
            elif cComment2.match(peice) and not inString:
                matchy = cComment2.match(peice)
                overall += matchy.group(1) 
                break

            elif cInclude.match(peice) and not inString:
                matchy = cInclude.match(peice)
                overall += f"import {(matchy.group(1)).strip().replace("\\", ".").replace("/", ".")}"
                break

            elif shortCutImportFrom.match(peice) and not inString:
                matchy = shortCutImportFrom.match(peice)
                modules = matchy.group(1)
                fromI = stdlib.clear_empty_gap(stdlib.split_arg(matchy.group(2)))
                overall += f"from {modules} import {", ".join(fromI)}"
                break

            elif shortCutImport.match(peice) and not inString:
                matchy = shortCutImport.match(peice)
                modules = stdlib.clear_empty_gap(stdlib.split_arg(matchy.group(1)))
                overall += f"import {", ".join(modules)}"
                break

            elif shortCutImportAs.match(peice) and not inString:
                matchy = shortCutImportAs.match(peice)
                modules = matchy.group(1)
                asModule = matchy.group(2)
                overall += f"import {modules} as {asModule}"
                break

            elif whenStatement.match(peice) and not inString:
                matchy = whenStatement.match(peice)
                state = matchy.group(1)
                overall += f"if {state}:"
                break

            if not inString:
                overall += peice[index]

            index += 1

        overall += "\n"
        currentLine += 1

    return overall

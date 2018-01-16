#!/usr/bin/python
# coding: utf-8
#BSD 2-Clause License
#
#Copyright (c) 2016, Eduard Bröcker
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#* Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
#* Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from lxml import etree
import sys
import chardet

if len(sys.argv) < 3:
    print("Syntax: %s infile.A2L outfile.XML" % sys.argv[0])
    exit()

inputFile = open(sys.argv[1],"r")
outputFile = open(sys.argv[2],"w")
inputBufRaw = inputFile.read()
encoding = chardet.detect(inputBufRaw)['encoding']
inputBuf = inputBufRaw.replace('\n', '').decode(encoding)

length = len(inputBuf)

types = ['int','uint','uint64','double','float','long','ulong','uchar','char']
trenner = [' ','[',']','{','}','(',')',',',';','=','\r','\n','/']
keywords = ['A2ML','A2ML_VERSION','ADDR_EPK','ALIGNMENT_BYTE','ALIGNMENT_FLOAT32_IEEE',
'ALIGNMENT_FLOAT64_IEEE','ALIGNMENT_INT64','ALIGNMENT_LONG','ALIGNMENT_WORD','ANNOTATION',
'ANNOTATION_LABEL','ANNOTATION_ORIGIN','ANNOTATION_TEXT','ARRAY_SIZE','ASAP2_VERSION',
'AXIS_DESCR','AXIS_PTS','AXIS_PTS_REF','AXIS_PTS_X','AXIS_PTS_Y','AXIS_PTS_Z','AXIS_PTS_4','AXIS_PTS_5',
'AXIS_RESCALE_X','BIT_MASK','BIT_OPERATION','BYTE_ORDER','CALIBRATION_ACCESS','CALIBRATION_HANDLE',
'CALIBRATION_HANDLE_TEXT','CALIBRATION_METHOD','CHARACTERISTIC','COEFFS','COEFFS_LINEAR','COMPARISON_QUANTITY',
'COMPU_METHOD','COMPU_TAB','COMPU_TAB_REF','COMPU_VTAB','COMPU_VTAB_RANGE','CPU_TYPE','CURVE_AXIS_REF',
'CUSTOMER','CUSTOMER_NO','DATA_SIZE','DEF_CHARACTERISTIC','DEFAULT_VALUE','DEFAULT_VALUE_NUMERIC',
'DEPENDENT_CHARACTERISTIC','DEPOSIT','DISCRETE','DISPLAY_IDENTIFIER','DIST_OP_X','DIST_OP_Z','DIST_OP_4',
'DIST_OP_5','ECU','ECU_ADDRESS','ECU_ADDRESS_EXTENSION','ECU_CALIBRATION_OFFSET','EPK','ERROR_MASK',
'EXTENDED_LIMITS','FIX_AXIS_PAR','FIX_AXIS_PAR_DIST','FIX_AXIS_PAR_LIST','FIX_NO_AXIS_PTS_X',
'FIX_NO_AXIS_PTS_Y','FIX_NO_AXIS_PTS_Z','FIX_NO_AXIS_PTS_4','FIX_NO_AXIS_PTS_5','FNC_VALUES','FORMAT',
'FORMULA','FORMULA_INV','FRAME','FRAME_MEASUREMENT','FUNCTION','FUNCTION_LIST','FUNCTION_VERSION',
'GROUP','GUARD_RAILS','HEADER','IDENTIFICATION','IF_DATA','IN_MEASUREMENT','LAYOUT','LEFT_SHIFT',
'LOC_MEASUREMENT','MAP_LIST','MATRIX_DIM','MAX_GRAD','MAX_REFRESH','MEASUREMENT','MEMORY_LAYOUT',
'MEMORY_SEGMENT','MOD_COMMON','MOD_PAR','MODULE','MONOTONY','NO_AXIS_PTS_X','NO_AXIS_PTS_Y','NO_AXIS_PTS_Z',
'NO_AXIS_PTS_4','NO_AXIS_PTS_5','NO_OF_INTERFACES','NO_RESCALE_X','NUMBER','OFFSET_X','OFFSET_Y','OFFSET_Z',
'OFFSET_4','OFFSET_5', 'OPTIONAL_CMD', 'OUT_MEASUREMENT','PHONE_NO','PHYS_UNIT','PROJECT','PROJECT_NO','READ_ONLY','READ_WRITE',
'RECORD_LAYOUT','REF_CHARACTERISTIC','REF_GROUP','REF_MEASUREMENT','REF_MEMORY_SEGMENT','REF_UNIT','RESERVED',
'RIGHT_SHIFT','RIP_ADDR_W','RIP_ADDR_X','RIP_ADDR_Y','RIP_ADDR_Z','RIP_ADDR_4','RIP_ADDR_5','ROOT','SHIFT_OP_X',
'SHIFT_OP_Y','SHIFT_OP_Z','SHIFT_OP_4','SHIFT_OP_5','SIGN_EXTEND','SI_EXPONENTS','SRC_ADDR_X','SRC_ADDR_Y',
'SRC_ADDR_Z','SRC_ADDR_4','SRC_ADDR_5','STATIC_RECORD_LAYOUT','STATUS_STRING_REF','STEP_SIZE','SUB_FUNCTION',
'SUB_GROUP','SUPPLIER','SYMBOL_LINK','SYSTEM_CONSTANT','UNIT','UNIT_CONVERSION','USER','USER_RIGHTS',
'VAR_ADDRESS','VAR_CHARACTERISTIC','VAR_CRITERION','VAR_FORBIDDEN_COMB','VAR_MEASUREMENT','VAR_NAMING',
'VAR_SELECTION_CHARACTERISTIC','VAR_SEPARATOR','VARIANT_CODING','VERSION','VIRTUAL','VIRTUAL_CHARACTERISTIC']

predefDataTypes = ['UBYTE','SBYTE','UWORD','SWORD','ULONG','SLONG','A_UINT64','A_INT64','FLOAT32_IEEE','FLOAT64_IEEE']
dataSizes = ['BYTE','WORD','LONG']
addrTypes = ['PBYTE','PWORD','PLONG','DIRECT']
byteOrders = ['LITTLE_ENDIAN','BIG_ENDIAN','MSB_LAST','MSB_FIRST']
indexOrders = ['INDEX_INCR', 'INDEX_DECR']
layoutTypes = ['ROW_DIR', 'COLUMN_DIR']
conversionTypes = ['IDENTICAL','FORM','LINEAR','RAT_FUNC','TAB_INTP','TAB_NOINTP','TAB_VERB']

def getNextToken(pos):
    while pos < length:
        if inputBuf[pos:pos+2] == "/*":
            pos = pos + 2
            startpos = pos
            while pos < length and not inputBuf[pos:pos+2] == '*/':
                pos = pos + 1
            pos = pos+2
#           return [pos, "COMMENT", inputBuf[startpos:pos]]
        elif inputBuf[pos] == '"':
            retStr = ""
            pos = pos + 1
            startpos = pos
            while pos < length and not inputBuf[pos] == '"':
                if inputBuf[pos] == '\\':
                    pos += 1
                retStr += inputBuf[pos]
                pos  += 1
            return [pos+1, "STRING", retStr]

        elif inputBuf[pos:pos+6] == "struct":
            return [pos+6, "STRUCT", ""]
        elif inputBuf[pos:pos+12] == "taggedstruct":
            return [pos+12, "TAGGEDSTRUCT", ""]
        elif inputBuf[pos:pos+11] == "taggedunion":
            return [pos+11, "TAGGEDUNION", ""]
        elif inputBuf[pos:pos+4] == "enum":
            return [pos+4, "ENUM", ""]
        elif inputBuf[pos:pos+6] == "/begin":
            return [pos+6, "BEGIN", ""]
        elif inputBuf[pos:pos+4] == "/end":
            return [pos+4, "END", ""]
        elif inputBuf[pos:pos+8] == "/include":
            return [pos+8, "INCLUDE", ""]
        elif inputBuf[pos] == "{":
            return [pos+1, "STARTBLOCK", ""]
        elif inputBuf[pos] == "}":
            return [pos+1, "ENDBLOCK", ""]
        elif inputBuf[pos] == "(":
            return [pos+1, "BEGINLIST", ""]
        elif inputBuf[pos] == ")":
            return [pos+1, "ENDLIST", ""]
        elif inputBuf[pos] == "[":
            return [pos+1, "BEGINDIM", ""]
        elif inputBuf[pos] == "]":
            return [pos+1, "ENDDIM", ""]
        elif inputBuf[pos] == ";":
            return [pos+1, "SEMICOL", ""]
        elif inputBuf[pos] == ",":
            return [pos+1, "COMMA", ""]
        elif inputBuf[pos] == "=":
            return [pos+1, "EQUAL", ""]
        elif inputBuf[pos] == "*":
            return [pos+1, "STAR",""]
        
#TODO block
        elif inputBuf[pos].isspace():
            pos = pos + 1
        else:
            startpos = pos
            while pos < length and not inputBuf[pos] in trenner:
                pos = pos + 1
            return [pos, "OUTLINE", inputBuf[startpos:pos]]
    return [pos,"ENDE", ""]

def processOutline(current, pos, outline):
    startPos = pos
    if outline == "ASAP2_VERSION":
        [pos, tt, mayor] = getNextToken(pos)
        if tt != "OUTLINE":
            return startPos
        [pos, tt, minor] = getNextToken(pos)
        if tt != "OUTLINE":
            return startPos
        current.append(etree.Element("ASAP2_VERSION", mayor=mayor, minor=minor))
        return pos
    elif outline in types:
        child = etree.Element("var", type=outline)
        [pos, tt, minor] = getNextToken(pos)
        while tt != "SEMICOL" and tt != "ENDLIST":
            if tt == "BEGINDIM":
                [pos, tt, out] = getNextToken(pos)
                child.attrib["dim"] = out
                while tt != "ENDDIM":
                    [pos, tt, minor] = getNextToken(pos)
                startPos = pos
            else:
                [pos, tt, minor] = getNextToken(pos)
        
        current.append(child)
        if tt == "ENDLIST":
            pos = startPos
        else:
            child = etree.Element("semicol")
            current.append(child)
    elif outline in keywords:
        child = etree.Element("keyword", type=outline)
        current.append(child)
    elif outline in predefDataTypes:
        child = etree.Element("datatype", type=outline)
        current.append(child)
    elif outline in dataSizes:
        child = etree.Element("dataSize", size=outline)
        current.append(child)
    elif outline in addrTypes:
        child = etree.Element("addrType", type=outline)
        current.append(child)
    elif outline in byteOrders:
        child = etree.Element("byteOrder", order=outline)
        current.append(child)
    elif outline in indexOrders:
        child = etree.Element("indexOrder", order=outline)
        current.append(child)
    elif outline in layoutTypes:
        child = etree.Element("layoutType", type=outline)
        current.append(child)
    elif outline in conversionTypes:
        child = etree.Element("conversionType", type=outline)
        current.append(child)
    else:
        child = etree.Element("item", type=outline)
        current.append(child)
        #pos = pos+1
#       if current.text is None:
#           current.text = outline
#       else:
#           current.text = str(current.text) + " " + outline
        pass
    return pos

def processBlock(current, pos, blkname):
    startPos = pos
    if blkname == "PROJECT" or blkname == "MODULE" or blkname == "COMPU_METHOD" or blkname == "MEASUREMENT":
        [pos, tt, name] = getNextToken(pos)
        if tt != "OUTLINE":
            return startPos
        current.attrib["name"] = name
        [pos, tt, comment] = getNextToken(pos)
        if tt == "BEGINDIM":
            [pos, tt, dimension] = getNextToken(pos)
            current.attrib["dim"] = dimension
            [pos, tt, dimension] = getNextToken(pos) # enddim
            [pos, tt, comment] = getNextToken(pos) # next should be comment
        if tt != "STRING":
            return startPos
        current.attrib["comment"] = comment
        return pos
    elif blkname == "IF_NAME":
        [pos, tt, proto] = getNextToken(pos)
        if tt != "OUTLINE":
            return startPos
        current.attrib["proto"] = proto
        return pos
    elif blkname == "IF_DATA":
        [pos, tt, interface] = getNextToken(pos)
        if tt != "OUTLINE":
            return startPos
        current.attrib["interface"] = interface
        return pos
    elif blkname == "HEADER" or blkname == "MOD_COMMON" or blkname == "MOD_PAR":
        [pos, tt, comment] = getNextToken(pos)
        if tt != "STRING":
            return startPos
        current.attrib["comment"] = comment
        return pos
    return startPos



root = etree.Element('a2l')
current = root
deepth = []
pos = 0

while pos < length:
    [pos, Token, outline] = getNextToken(pos)
    if  pos < length:
        [pos2, Token2, outline2] = getNextToken(pos)
    else:
        pos2 = length
        Token2 = ""
        outline2 = ""

    if Token2 == "EQUAL":
        [pos3, Token3, outline3] = getNextToken(pos2)
        child = etree.Element("equals",  rval = outline3, lval = outline)
        current.append(child)
        pos = pos3
        continue
        pass
    if Token == "COMMENT":
        child = etree.Comment(outline)
        current.append(child)
    elif Token == "BEGIN":
        [pos, tt, blockname] = getNextToken(pos)
        child = etree.Element(blockname)
        current.append(child)
        deepth.append(current)
        current = child
        pos = processBlock(current, pos, blockname)
    elif Token == "END":
        [pos, tt, blockname] = getNextToken(pos)
        try:
            current = deepth.pop()
        except:
            print("Error witch closing: " + inputBuf[pos-100:pos+100])
    elif Token == "INCLUDE":
        [pos, tt, blockname] = getNextToken(pos)
        child = etree.Element("include")
        child.attrib["file"] = blockname
        current.append(child)
    elif Token == "STARTBLOCK":
        child = etree.Element("block")
        current.append(child)
        deepth.append(current)
        current = child
        pass
    elif Token == "ENDBLOCK":
        try:
            current = deepth.pop()
        except:
            print("Error witch closing: " + inputBuf[pos-10:pos+10])
    elif Token == "TAGGEDSTRUCT":
        child = etree.Element('taggedstruct')
        current.append(child)
        #deepth.append(current)
        #current = child
        [pos2, tt, structName] = getNextToken(pos)
        if tt == "OUTLINE":
            current.attrib["name"] = structName
            pos = pos2
    elif Token == "TAGGEDUNION":
        child = etree.Element('taggedunion')
        current.append(child)
        #deepth.append(current)
        #current = child
        [pos2, tt, structName] = getNextToken(pos)
        if tt == "OUTLINE":
            child.attrib["name"] = structName
            pos = pos2
    elif Token == "STRUCT":
        child = etree.Element('struct')
        current.append(child)
        #deepth.append(current)
        #current = child
        [pos2, tt, structName] = getNextToken(pos)
        if tt == "OUTLINE":
            child.attrib["name"] = structName
            pos = pos2
    elif Token == "ENUM":
        child = etree.Element('enum')
        current.append(child)
        #deepth.append(current)
        #current = child
    elif Token == "SEMICOL":
        child = etree.Element('semicol')
        current.append(child)
#       current.text = str(current.text) + ";"
    elif Token == "COMMA":
#       current.text = str(current.text) + ","
        pass
    elif Token == "EQUAL":
#       current.text = str(current.text) + " = "
        pass
    elif Token == "STRING":
        child = etree.Element("string", value = outline)
        current.append(child)

#       if current.text is None:
#           current.text = outline
#       else:
#           current.text = str(current.text) + " " + outline
        pass
    elif Token == "OUTLINE":
        pos = processOutline(current, pos, outline)
        pass
    elif Token == "BEGINLIST":
        child = etree.Element('list')
        current.append(child)
        deepth.append(current)
        current = child
    elif Token == "ENDLIST":
        current = deepth.pop()
    elif Token == "STAR":
        child = etree.Element("star")
        current.append(child)
    elif Token == "BEGINDIM":
        [pos, tt, out] = getNextToken(pos)
        if len(current.getchildren()) > 0:
            current.getchildren()[-1].attrib["dim"] = out
        else:
            current.attrib["dim"] = out
        while tt != "ENDDIM":
            [pos, tt, minor] = getNextToken(pos)
    elif Token == "ENDE":
        pass

    else:
        print "#" + Token + "# ??"

s = etree.tostring(root, pretty_print=True)
outputFile.write(s)


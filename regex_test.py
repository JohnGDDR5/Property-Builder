
import re
"""
def getDirectionRegEx(string, type=None):
    
    pattern = '(?<=[ \.\-_])[rRlL]((?=$|[ \.\-_])|(?i)(ight|eft))'
    
    #print("pattern: %s" % (pattern) )
    rawString = r'%s' % (pattern)
    
    #print("rawString: %s" % (rawString) )
    
    #compiled RegEx object
    regex = re.compile(rawString)
    
    
    match = regex.search(string)
    
    if type == "STRING":
        matchString = match.group(0)
        return matchString
    else:
        return match
"""

string = "Leg.Left.Back"

#pattern = '.[rRlL](\?)'
#pattern = '(?<=[ \.\-_])[rRlL]((?=$|[ \.\-_])|(?i)(ight|eft))'
pattern = '(?i)(?<=[ \.\-_])[rRlL]((?=$|[ \.\-_])|(ight|eft))'

rawPattern = r'%s' % (pattern)

object = re.search(rawPattern, string)

print(string)

## a regex object
print(object)
##print <re.Match object; span=(3, 5), match='.L'>

##Using .group()
print(object.group() )
print(object.group(0) )
##Prints ".L"

##Using .span()
print(object.span() )
##Prints a tuple with the start & end index of the match from previous string
##Prints (3, 5)


##To efficiently use ReGex, compile a RE into an object, and use that object to compare string, this saves a ton of time.

#Ex.
p = re.compile(rawPattern)
##Returns a Match object
print(p)
print(p.__class__)

object = p.search(string)

print(object.string )

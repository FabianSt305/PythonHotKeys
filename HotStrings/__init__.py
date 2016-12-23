import keyboard
import re

"""
Hotstring Options
* (asterisk): An ending character (e.g. space, period, or enter) is not required
	to trigger the hotstring.

? (question mark): The hotstring will be triggered even when it is inside
	another word; that is, when the character typed immediately before it is
	alphanumeric.

B0 (B followed by a zero): Automatic backspacing is not done to erase the
	abbreviation you type.

C: Case sensitive: When you type an abbreviation, it must exactly match the case
	defined in the script.

C0 (C followed by a zero): Turn case sensitivity off.

C1: Do not conform to typed case.

O: Omit the ending character.

R: Send the replacement text raw; that is, exactly as it appears rather than
	translating {Enter} to an ENTER keystroke, ^c to Control-C, etc.
"""


def main():
    with open('config', 'r') as config:
        hotstring_config = [line.strip() for line in config.readlines()]

    for line in hotstring_config:
        hotstring = re.match(r':(.*):(.+)::(.+)', line)
        if hotstring is not None:
            options = hotstring.group(1)
            trigger = hotstring.group(2)
            action = hotstring.group(3)

            add_hotstring(trigger, action, options)

            # print "options:", options
            # print "trigger:", trigger
            # print "action:", action


def add_hotstring(source_text, replacement_text, options="",
                  match_suffix=True, timeout=2):
    """
    copy of add_abbreviation to add a delay to the callback so that spaces are
    not skipped
    Also adding a switch between a hotkey like behavior and a word listener
    """
    if "*" in options:
        trigger = ",".join(c for c in source_text)
        replacement = '\b'*len(source_text) + replacement_text
        callback = lambda: keyboard.write(replacement,
                                          delay=.01, restore_state_after=False)
        return keyboard.add_hotkey(trigger, callback,
                                   timeout=timeout)
    else:
        triggers = ['space','enter','tab']
        # AHK HotString end characters -()[]{}:;'"/\,.?!`n `t
        replacement = '\b'*(len(source_text)+1) + replacement_text
        callback = lambda: keyboard.write(replacement,
                                          delay=.01, restore_state_after=False)
        return keyboard.add_word_listener(source_text, callback,
                                          triggers=triggers,
                                          match_suffix=match_suffix,
                                          timeout=timeout)

main()

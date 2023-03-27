# Command Center

The purpose of this module is to facilitate which command should be executed based on the given intent and pass along the rest of the users command to the given 
module.

Intent and user commands are the input (redis message)
Validation is done to understand if the intent is supported
If supported:
kick off the subprocess or docker container which is designated for that intent
Display to the user that the tasking is successful (debug purposes only)

If not supported:
Inform the user that either the intent is unknown or unsupported at this time



Questions:
- Does the command center deal with cleanup of the command as well? (probably)

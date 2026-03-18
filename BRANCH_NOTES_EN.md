An attempt to improve the work with CEF. Now Browser works as planned initially. I will be glad to comments / suggestions on improving the current code.

Example [./server/python/__init\__.py](https://github.com/ackut/PySAMP-CEF/blob/18d3eda4ea8730b4efb18c81a243d7562fbcc91e/server/python/__init__.py)


# Key features and limitations.
### 1. Compatibility with a specific build of CEF
The code only works with `cef.dll` / `cef.so` from the repository - these builds have some kind of fix (I don't remember which, in my opinion it was done by Cheaterman). Recently [samp-cef](https://github.com/zottce/samp-cef) was updated, it is possible that the fix is already included, but there is no official release yet - manual build is required.

### 2. Serialization of data in JSON
Due to the features of [samp-cef](https://github.com/zottce/samp-cef), all data passed to events are packed into a JSON string and passed as a single argument.
* On the Python side, it uses `json.dumps` / `json.loads`.
* It is expected that the data is always a string that contains a dictionary (Python `dict` or TypeScript `Record<any, any>`).

### 3. Browser ID `==` Player ID
Using multiple browsers per player is [not recommended](https://github.com/zottce/samp-cef/blob/refresh-code/docs/main_en.md#tips-and-some-limitations), so I made this decision, and at the moment I don't see any reason to change it.


# Initialization process
1. `Player.on_connect` -> `Browser.init_cef` (initialization of CEF for the player)
2. `Browser.on_cef_init` -> `Browser.create`
3. `Browser.on_created` -> the browser is created, but this does not mean that the site page is loaded
4. `Browser.on("cef::dom::ready")` -> the browser is fully ready to work (this event you implement yourself)


# Plans for hashing event names
I'm not sure, but it is possible that CEF has a limit on the length of the event name, or long names will create an excessive load.

Therefore, it is worth implementing a hashing mechanism `{"event:name": "b563b034d07", ...`}`, and then a handshake mechanism where the client and server exchange "event maps" when the player connects.
I don't have enough experience with TypeScript (on the client) to implement this, at least not yet.

# Client wrapper
I already have a client wrapper for CEF (Vue 3, TypeScript, Pinia, Vue Router), but I'm not ready to upload it to GitHub yet. It needs further development.
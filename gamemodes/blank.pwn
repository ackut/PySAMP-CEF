#include <open.mp>
#include <cef>

main(){}

forward CefEmitEvent(player_id, const event[], const args[]);
public CefEmitEvent(player_id, const event[], const args[]) {
	cef_emit_event(player_id, event, CEFSTR(args));
    return 0;
}
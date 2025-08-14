const ws_url = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';

let socket: WebSocket | null = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

export const websocketService = {
    connect(token: string) {
        if (socket && socket.readyState === WebSocket.OPEN) return;

        socket = new WebSocket(`${ws_url}?token=${token}`);

        socket.onopen = () => {
            console.log('WebSocket connected');
            reconnectAttempts = 0;
        };

        socket.onclose = (event: CloseEvent) => {
            console.log(`WebSocket closed: ${event.reason}`);
            socket = null;
            if (reconnectAttempts < maxReconnectAttempts) {
                setTimeout(() => {
                    reconnectAttempts++;
                    this.connect(token);
                }, 1000 * reconnectAttempts);
            }
        };

        socket.onerror = (error: Event) => {
            console.error('WebSocket error:', error);
            socket?.close();
        };
    },

    disconnect() {
        if (socket) {
            socket.close();
        }
    },

    onMessage(callback: (data: any) => void) {
        if (socket) {
            socket.onmessage = (event: MessageEvent) => {
                try {
                    const data = JSON.parse(event.data);
                    callback(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
        }
    }
};

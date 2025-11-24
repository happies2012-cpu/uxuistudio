import app from './app';
import { createServer } from 'http';
import { Server } from 'socket.io';
import logger from './config/logger';

const PORT = process.env.PORT || 3001;

const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: '*', // Allow all for dev
        methods: ['GET', 'POST']
    }
});

// Socket.io connection handler
io.on('connection', (socket) => {
    logger.info(`Socket connected: ${socket.id}`);

    socket.on('join-site', (siteId) => {
        socket.join(`site:${siteId}`);
        logger.info(`Socket ${socket.id} joined site:${siteId}`);
    });

    socket.on('disconnect', () => {
        logger.info(`Socket disconnected: ${socket.id}`);
    });
});

// Make io accessible globally or via context (simplified here)
export { io };

httpServer.listen(PORT, () => {
    logger.info(`🚀 Node.js Backend running on port ${PORT}`);
});

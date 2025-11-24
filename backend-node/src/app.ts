import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { errorHandler } from './middleware/error';
import authRoutes from './routes/auth.routes';
import siteRoutes from './routes/site.routes';

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/sites', siteRoutes);

// Health Check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'node-backend' });
});

// Error Handling
app.use(errorHandler);

export default app;

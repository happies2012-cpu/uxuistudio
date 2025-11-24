import prisma from '../config/prisma';
import axios from 'axios';
import https from 'https';
import { AppError } from '../middleware/error';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'https://localhost:8000';

// Agent to ignore self-signed certs in dev
const httpsAgent = new https.Agent({
    rejectUnauthorized: false
});

export class SiteService {
    async createSite(userId: string, data: any) {
        // 1. Create Site record in DB (status: GENERATING)
        const site = await prisma.site.create({
            data: {
                name: data.business_name,
                businessType: data.business_type,
                description: data.description,
                status: 'GENERATING',
                userId
            }
        });

        // 2. Call Python AI Engine to start generation
        try {
            const response = await axios.post(
                `${PYTHON_API_URL}/api/v1/sites/generate`,
                {
                    ...data,
                    webhook_url: `http://localhost:3001/api/v1/sites/${site.id}/webhook` // Callback URL
                },
                { httpsAgent }
            );

            // Update site with job ID if needed
            // await prisma.site.update(...)

            return { site, job_id: response.data.job_id };
        } catch (error) {
            // If AI call fails, mark site as failed
            await prisma.site.update({
                where: { id: site.id },
                data: { status: 'FAILED' }
            });
            throw new AppError('Failed to start site generation', 500);
        }
    }

    async listSites(userId: string) {
        return prisma.site.findMany({
            where: { userId },
            orderBy: { createdAt: 'desc' }
        });
    }

    async getSite(siteId: string, userId: string) {
        const site = await prisma.site.findFirst({
            where: { id: siteId, userId }
        });
        if (!site) throw new AppError('Site not found', 404);
        return site;
    }
}

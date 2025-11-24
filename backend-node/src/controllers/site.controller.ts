import { Response, NextFunction } from 'express';
import { AuthRequest } from '../middleware/auth';
import { SiteService } from '../services/site.service';

const siteService = new SiteService();

export const createSite = async (req: AuthRequest, res: Response, next: NextFunction) => {
    try {
        const result = await siteService.createSite(req.user.id, req.body);
        res.status(201).json(result);
    } catch (error) {
        next(error);
    }
};

export const listSites = async (req: AuthRequest, res: Response, next: NextFunction) => {
    try {
        const sites = await siteService.listSites(req.user.id);
        res.json(sites);
    } catch (error) {
        next(error);
    }
};

export const getSite = async (req: AuthRequest, res: Response, next: NextFunction) => {
    try {
        const site = await siteService.getSite(req.params.id, req.user.id);
        res.json(site);
    } catch (error) {
        next(error);
    }
};

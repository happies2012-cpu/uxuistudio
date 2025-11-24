import { Router } from 'express';
import { createSite, listSites, getSite } from '../controllers/site.controller';
import { authenticate } from '../middleware/auth';

const router = Router();

router.use(authenticate); // Protect all routes

router.post('/generate', createSite); // Map generate to createSite
router.get('/', listSites);
router.get('/:id', getSite);

export default router;

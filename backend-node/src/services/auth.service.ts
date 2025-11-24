import prisma from '../config/prisma';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { AppError } from '../middleware/error';

const JWT_SECRET = process.env.JWT_SECRET || 'supersecret';

export class AuthService {
    async register(data: any) {
        const { email, password, name } = data;

        const existingUser = await prisma.user.findUnique({ where: { email } });
        if (existingUser) {
            throw new AppError('User already exists', 400);
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await prisma.user.create({
            data: {
                email,
                password: hashedPassword,
                firstName: name, // Map name to firstName for now
            },
        });

        const token = this.generateToken(user.id);
        return { user: { id: user.id, email: user.email, name: user.firstName }, token };
    }

    async login(data: any) {
        const { email, password } = data;

        const user = await prisma.user.findUnique({ where: { email } });
        if (!user) {
            throw new AppError('Invalid credentials', 401);
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            throw new AppError('Invalid credentials', 401);
        }

        const token = this.generateToken(user.id);
        return { user: { id: user.id, email: user.email, name: user.firstName }, token };
    }

    private generateToken(userId: string) {
        return jwt.sign({ id: userId }, JWT_SECRET, { expiresIn: '7d' });
    }
}

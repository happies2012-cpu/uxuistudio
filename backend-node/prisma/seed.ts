import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
    console.log('🌱 Starting seeding...');

    // 1. Create Admin User
    const adminEmail = 'admin@gswstudio.ai';
    const existingAdmin = await prisma.user.findUnique({ where: { email: adminEmail } });

    if (!existingAdmin) {
        const hashedPassword = await bcrypt.hash('admin123', 10);
        await prisma.user.create({
            data: {
                email: adminEmail,
                password: hashedPassword,
                name: 'Admin User',
                role: 'ADMIN',
                emailVerified: true,
            },
        });
        console.log('✅ Admin user created');
    }

    // 2. Create Themes
    const themes = [
        {
            name: 'Astra',
            slug: 'astra',
            description: 'Fast, lightweight, and highly customizable WordPress theme.',
            thumbnail: 'https://ps.w.org/astra/assets/screenshot.jpg',
            version: '4.6.0',
            isPremium: false,
        },
        {
            name: 'OceanWP',
            slug: 'oceanwp',
            description: 'Perfect theme for your project. Lightweight and highly extendable.',
            thumbnail: 'https://ps.w.org/oceanwp/assets/screenshot.png',
            version: '3.5.0',
            isPremium: false,
        },
        {
            name: 'Divi',
            slug: 'divi',
            description: 'The most popular WordPress theme in the world and the ultimate WordPress Page Builder.',
            thumbnail: 'https://www.elegantthemes.com/images/divi/divi-builder.jpg',
            version: '4.23.0',
            isPremium: true,
            price: 89.00,
        }
    ];

    for (const theme of themes) {
        await prisma.theme.upsert({
            where: { slug: theme.slug },
            update: {},
            create: theme,
        });
    }
    console.log(`✅ ${themes.length} themes seeded`);

    // 3. Create Plugins
    const plugins = [
        {
            name: 'Elementor',
            slug: 'elementor',
            description: 'The Elementor Website Builder has it all: drag and drop page builder, pixel perfect design, mobile responsive editing, and more.',
            category: 'Page Builder',
            required: false,
        },
        {
            name: 'Yoast SEO',
            slug: 'wordpress-seo',
            description: 'Improve your WordPress SEO: Write better content and have a fully optimized WordPress site.',
            category: 'SEO',
            required: true,
        },
        {
            name: 'WooCommerce',
            slug: 'woocommerce',
            description: 'WooCommerce is the world’s most popular open-source eCommerce solution.',
            category: 'E-commerce',
            required: false,
        },
        {
            name: 'Contact Form 7',
            slug: 'contact-form-7',
            description: 'Just another contact form plugin. Simple but flexible.',
            category: 'Forms',
            required: false,
        }
    ];

    for (const plugin of plugins) {
        await prisma.plugin.upsert({
            where: { slug: plugin.slug },
            update: {},
            create: plugin,
        });
    }
    console.log(`✅ ${plugins.length} plugins seeded`);

    console.log('🌱 Seeding completed.');
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });

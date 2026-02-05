'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AnimatedWrapper } from '@/components/ui/animated-wrapper';
import {
  ArrowRight,
  CheckCircle,
  Star,
  Zap,
  Shield,
  Palette,
  Layout,
  Code
} from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { user, loading } = useAuth();

  const features = [
    {
      icon: <Palette className="h-6 w-6" />,
      title: "Modern Design",
      description: "Clean, elegant UI with premium aesthetics"
    },
    {
      icon: <Layout className="h-6 w-6" />,
      title: "Responsive Layout",
      description: "Perfectly adapts to all screen sizes"
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: "Developer Friendly",
      description: "Easy to customize and extend"
    }
  ];

  const searchParams = useSearchParams();
  const showLanding = searchParams.get('showLanding') === 'true';

  // If user is authenticated, redirect to dashboard (unless explicitly requesting to show landing page)
  useEffect(() => {
    if (!loading && user && !showLanding) {
      router.push('/dashboard');
    }
  }, [user, loading, router, showLanding]);

  // Don't render anything during auth check or when user is authenticated (unless showing landing explicitly)
  if (loading || (user && !showLanding)) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <AnimatedWrapper type="fadeIn" delay={0.1}>
          <div className="max-w-4xl mx-auto text-center mb-16">
            <Badge variant="secondary" className="mb-4">v1.0.0</Badge>
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent dark:from-primary-400 dark:to-primary-300 mb-6">
              Premium Task Management
            </h1>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 mb-8 max-w-2xl mx-auto">
              A beautifully crafted task management application with elegant design and seamless user experience.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/sign-up">
                <Button size="lg" className="px-8 py-3 text-base">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
              <Link href="/sign-in">
                <Button variant="outline" size="lg" className="px-8 py-3 text-base">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </AnimatedWrapper>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <AnimatedWrapper key={feature.title} type="slideIn" direction="up" delay={index * 0.1}>
              <Card className="text-center hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <div className="mx-auto p-3 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                    <div className="text-primary-600 dark:text-primary-400">
                      {feature.icon}
                    </div>
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            </AnimatedWrapper>
          ))}
        </div>

        {/* Call to Action */}
        <AnimatedWrapper type="fadeIn" delay={0.6}>
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to boost your productivity?</h2>
            <p className="text-lg text-neutral-600 dark:text-neutral-300 mb-8 max-w-2xl mx-auto">
              Join thousands of satisfied users who trust our platform for their daily task management.
            </p>
            <Link href="/sign-up">
              <Button size="lg" className="px-8 py-3 text-base">
                Start Free Trial <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </AnimatedWrapper>
      </div>
    </div>
  );
}
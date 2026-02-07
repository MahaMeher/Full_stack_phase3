'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';

export default function LandingChecker() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const searchParams = useSearchParams();
  const showLanding = searchParams.get('showLanding') === 'true';

  // If user is authenticated, redirect to dashboard (unless explicitly requesting to show landing page)
  useEffect(() => {
    if (!loading && user && !showLanding) {
      router.push('/dashboard');
    }
  }, [user, loading, router, showLanding]);

  return null;
}
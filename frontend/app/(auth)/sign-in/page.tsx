'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { loginSchema, type LoginFormData } from '@/lib/validations';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const router = useRouter();
  const { login, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});

    // Validate input
    try {
      loginSchema.parse({ email, password });
    } catch (validationError: any) {
      const fieldErrors: Record<string, string> = {};
      if (validationError.errors) {
        validationError.errors.forEach((error: any) => {
          fieldErrors[error.path[0]] = error.message;
        });
      }
      setErrors(fieldErrors);
      return;
    }

    // Attempt login
    const result = await login(email, password);
    if (result.success) {
      // Redirect to dashboard
      router.push('/dashboard');
      router.refresh(); // Refresh to update the UI
    } else {
      setErrors({ general: result.error || 'Login failed' });
    }
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <CardTitle className="text-2xl font-bold text-foreground">Sign In</CardTitle>
        <CardDescription className="mt-2 text-foreground/80">
          Enter your credentials to access your account
        </CardDescription>
      </div>

      <CardContent className="p-0">
        <form onSubmit={handleSubmit} className="space-y-4">
          {errors.general && (
            <div className="text-red-500 text-sm">{errors.general}</div>
          )}

          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={errors.email ? 'border-red-500' : 'bg-white/90 dark:bg-gray-800/90'}
            />
            {errors.email && (
              <p className="text-red-500 text-sm">{errors.email}</p>
            )}
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={errors.password ? 'border-red-500' : 'bg-white/90 dark:bg-gray-800/90'}
            />
            {errors.password && (
              <p className="text-red-500 text-sm">{errors.password}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="mt-4 text-center text-sm">
          Don't have an account?{' '}
          <Link href="/sign-up" className="text-primary hover:underline">
            Sign up
          </Link>
        </div>
      </CardContent>
    </div>
  );
}
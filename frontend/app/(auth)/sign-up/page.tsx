'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { registerSchema, type RegisterFormData } from '@/lib/validations';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';
import PasswordRequirements from '@/components/auth/password-requirements';

export default function SignUpPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const router = useRouter();
  const { register, loading } = useAuth();

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handlePasswordFocus = () => {
    setShowPasswordRequirements(true);
  };

  const handlePasswordBlur = () => {
    setShowPasswordRequirements(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});

    // Validate input
    try {
      registerSchema.parse({ name, email, password });
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

    // Attempt registration
    const result = await register(name, email, password);
    if (result.success) {
      // Redirect to login page after successful registration
      router.push('/sign-in');
    } else {
      setErrors({ general: result.error || 'Registration failed' });
    }
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <CardTitle className="text-2xl font-bold text-foreground">Sign Up</CardTitle>
        <CardDescription className="mt-2 text-foreground/80">
          Create an account to get started
        </CardDescription>
      </div>

      <CardContent className="p-0">
        <form onSubmit={handleSubmit} className="space-y-4">
          {errors.general && (
            <div className="text-red-500 text-sm">{errors.general}</div>
          )}

          <div className="space-y-2">
            <label htmlFor="name" className="text-sm font-medium">
              Full Name
            </label>
            <Input
              id="name"
              type="text"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className={errors.name ? 'border-red-500 bg-white/90 dark:bg-gray-800/90' : 'bg-white/90 dark:bg-gray-800/90'}
            />
            {errors.name && (
              <p className="text-red-500 text-sm">{errors.name}</p>
            )}
          </div>

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
              className={errors.email ? 'border-red-500 bg-white/90 dark:bg-gray-800/90' : 'bg-white/90 dark:bg-gray-800/90'}
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
              onChange={handlePasswordChange}
              onFocus={handlePasswordFocus}
              onBlur={handlePasswordBlur}
              className={errors.password ? 'border-red-500 bg-white/90 dark:bg-gray-800/90' : 'bg-white/90 dark:bg-gray-800/90'}
            />
            {showPasswordRequirements && (
              <PasswordRequirements password={password} isVisible={showPasswordRequirements} />
            )}
            {errors.password && (
              <p className="text-red-500 text-sm">{errors.password}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign Up'}
          </Button>
        </form>

        <div className="mt-4 text-center text-sm">
          Already have an account?{' '}
          <Link href="/sign-in" className="text-primary hover:underline">
            Sign in
          </Link>
        </div>
      </CardContent>
    </div>
  );
}
'use client';

import { useState, useEffect } from 'react';

interface PasswordRequirementsProps {
  password: string;
  isVisible?: boolean;
}

export default function PasswordRequirements({
  password,
  isVisible = true
}: PasswordRequirementsProps) {
  const [requirements, setRequirements] = useState([
    { id: 'length', text: 'At least 8 characters', met: false },
    { id: 'uppercase', text: 'One uppercase letter (A-Z)', met: false },
    { id: 'lowercase', text: 'One lowercase letter (a-z)', met: false },
    { id: 'digit', text: 'One digit (0-9)', met: false },
    { id: 'special', text: 'One special character (!@#$%^&*(),.?":{}|<>)', met: false },
  ]);

  useEffect(() => {
    const updatedRequirements = requirements.map(req => {
      switch (req.id) {
        case 'length':
          return { ...req, met: password.length >= 8 };
        case 'uppercase':
          return { ...req, met: /[A-Z]/.test(password) };
        case 'lowercase':
          return { ...req, met: /[a-z]/.test(password) };
        case 'digit':
          return { ...req, met: /\d/.test(password) };
        case 'special':
          return { ...req, met: /[!@#$%^&*(),.?":{}|<>]/.test(password) };
        default:
          return req;
      }
    });

    setRequirements(updatedRequirements);
  }, [password]);

  if (!isVisible) return null;

  return (
    <div className="mt-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-700 text-xs">
      <p className="font-medium text-gray-700 dark:text-gray-300 mb-1">Password must contain:</p>
      <ul className="space-y-1">
        {requirements.map((req) => (
          <li key={req.id} className="flex items-center">
            <span className={`mr-2 ${req.met ? 'text-green-500' : 'text-gray-400'}`}>
              {req.met ? '✓' : '○'}
            </span>
            <span className={`${req.met ? 'text-green-700 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'}`}>
              {req.text}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
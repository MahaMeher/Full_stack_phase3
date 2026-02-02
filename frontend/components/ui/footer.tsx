import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-lg font-semibold">Todo App</h3>
            <p className="text-sm text-gray-400 mt-1">Your productivity partner</p>
          </div>

          <div className="flex flex-wrap justify-center gap-6 mb-4 md:mb-0">
            <nav>
              <ul className="flex flex-wrap gap-4 text-sm">
                <li><Link href="/" className="hover:text-blue-300 transition-colors">Home</Link></li>
                <li><Link href="/dashboard" className="hover:text-blue-300 transition-colors">Dashboard</Link></li>
                <li><Link href="/sign-in" className="hover:text-blue-300 transition-colors">Sign In</Link></li>
                <li><Link href="/sign-up" className="hover:text-blue-300 transition-colors">Sign Up</Link></li>
              </ul>
            </nav>
          </div>

          <div className="flex space-x-4">
            <Button variant="outline" size="sm" className="border-gray-600 text-white hover:bg-gray-700 text-xs">
              Terms
            </Button>
            <Button variant="outline" size="sm" className="border-gray-600 text-white hover:bg-gray-700 text-xs">
              Privacy
            </Button>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-6 pt-4 text-center text-xs text-gray-400">
          <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
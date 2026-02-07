'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function TermsPage() {
  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Terms of Service</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-foreground">
          <section className="space-y-2">
            <h2 className="text-xl font-semibold">1. Acceptance of Terms</h2>
            <p>
              By accessing and using this application, you accept and agree to be bound by the terms and provision of this agreement.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">2. Use License</h2>
            <p>
              Permission is granted to temporarily download one copy of the materials on our application for personal, non-commercial transitory viewing only.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">3. Disclaimer</h2>
            <p>
              The materials on our application are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">4. Limitations</h2>
            <p>
              In no event shall we or our directors, employees, or agents be liable for any loss of profits or any indirect, incidental, consequential, or special damages arising out of or in connection with your use of our application.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">5. Accuracy of Materials</h2>
            <p>
              The materials appearing on our application could include technical, typographical, or photographic errors. We do not warrant that any of the materials on our application are accurate, complete, or current.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">6. Links</h2>
            <p>
              Our application may contain links to external websites. We have no control over the nature, content, and availability of those sites and are not responsible for any information, materials, products, or services on or available from those sites.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">7. Modifications</h2>
            <p>
              We reserve the right to modify these terms of service at any time. You are advised to review this page periodically for any changes.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">8. Governing Law</h2>
            <p>
              These terms and conditions are governed by and construed in accordance with the laws of our jurisdiction and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  );
}
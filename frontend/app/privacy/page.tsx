'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function PrivacyPage() {
  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Privacy Policy</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-foreground">
          <section className="space-y-2">
            <h2 className="text-xl font-semibold">1. Information We Collect</h2>
            <p>
              We collect information you provide directly to us, such as when you create an account, use our services, or contact us for support. This may include your name, email address, and other information you choose to provide.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">2. How We Use Information</h2>
            <p>
              We use information we collect to provide, maintain, and improve our services, to communicate with you, and to protect our users and the public. We do not share your personal information with third parties except as described in this policy.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">3. Information Sharing</h2>
            <p>
              We do not share your personal information with companies, organizations, or individuals outside of our organization except in the following limited circumstances:
            </p>
            <ul className="list-disc pl-6 space-y-1">
              <li>With your consent</li>
              <li>To comply with applicable law, regulation, legal process or governmental request</li>
              <li>To enforce our terms and conditions</li>
              <li>To protect our rights, privacy, safety, or property, and that of our users</li>
            </ul>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">4. Data Security</h2>
            <p>
              We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">5. Data Retention</h2>
            <p>
              We retain your personal information for as long as necessary to provide our services and comply with our legal obligations. When we no longer need your information, we will securely delete it.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">6. Cookies and Similar Technologies</h2>
            <p>
              We may use cookies and similar technologies to provide and improve our services. You can control cookies through your browser settings.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">7. Your Rights</h2>
            <p>
              Depending on your location, you may have rights regarding your personal information, including the right to access, correct, or delete your information. Contact us to exercise these rights.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">8. Children's Privacy</h2>
            <p>
              Our services are not directed to children under the age of 13. We do not knowingly collect personal information from children under 13.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">9. Changes to This Policy</h2>
            <p>
              We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the effective date.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-xl font-semibold">10. Contact Us</h2>
            <p>
              If you have questions about this privacy policy, please contact us using the information provided in our contact section.
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  );
}
'use client'

import { useRouter } from 'next/navigation'
import { HeroSection } from '@/components/homepage/HeroSection'
import { FeaturesSection } from '@/components/homepage/FeaturesSection'
import { HowItWorksSection } from '@/components/homepage/HowItWorksSection'
import { CTASection } from '@/components/homepage/CTASection'
import { Footer } from '@/components/layout/Footer'
import { useAuth } from '@/providers/AuthProvider'

export default function HomePage() {
  const router = useRouter()
  const { isAuthenticated, loading } = useAuth()

  const features = [
    {
      id: '1',
      title: 'AI-Powered Task Suggestions',
      description: 'Get intelligent recommendations for organizing and prioritizing your tasks based on your patterns and preferences.',
      icon: 'sparkles'
    },
    {
      id: '2',
      title: 'Smart Categorization & Priorities',
      description: 'Automatically categorize tasks and set priorities to focus on what matters most.',
      icon: 'tags'
    },
    {
      id: '3',
      title: 'Cross-Device Synchronization',
      description: 'Access your tasks seamlessly across all your devices with real-time sync.',
      icon: 'refresh'
    },
    {
      id: '4',
      title: 'Productivity Analytics',
      description: 'Track your progress and gain insights into your productivity patterns over time.',
      icon: 'chart'
    }
  ]

  const steps = [
    {
      number: 1,
      title: 'Sign Up & Create Your First Task',
      description: 'Get started in seconds with a simple registration process and add your first task.'
    },
    {
      number: 2,
      title: 'Organize with Categories & Priorities',
      description: 'Use smart categories and priority levels to keep your tasks organized and focused.'
    },
    {
      number: 3,
      title: 'Get AI-Powered Insights',
      description: 'Receive intelligent suggestions and analytics to boost your productivity.'
    }
  ]

  const footerLinks = [
    { label: 'About', href: '/about' },
    { label: 'Privacy Policy', href: '/privacy' },
    { label: 'Terms of Service', href: '/terms' },
    { label: 'Contact', href: '/contact' }
  ]

  const handleSignUp = () => {
    router.push('/register')
  }

  const handleLogin = () => {
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-pulse text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <HeroSection
        title="AI Powered Todo Web App"
        subtitle="Manage your tasks efficiently with intelligent organization and insights"
        primaryCTA="Sign Up"
        secondaryCTA="Login"
        onPrimaryCTAClick={handleSignUp}
        onSecondaryCTAClick={handleLogin}
        isAuthenticated={isAuthenticated}
      />

      <FeaturesSection
        features={features}
        heading="Powerful Features for Productivity"
        subheading="Everything you need to stay organized and focused"
      />

      <HowItWorksSection
        steps={steps}
        heading="How It Works"
      />

      <CTASection
        heading="Ready to boost your productivity?"
        description="Join thousands of users who are already managing their tasks more efficiently."
        buttonText="Get Started Free"
        onButtonClick={handleSignUp}
      />

      <Footer
        links={footerLinks}
        copyright={`© ${new Date().getFullYear()} AI Powered Todo. All rights reserved.`}
      />
    </div>
  )
}

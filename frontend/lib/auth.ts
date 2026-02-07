// Mock auth implementation that uses the backend's auth endpoint to generate tokens
// This simulates the auth functions that would come from Better Auth

export interface Session {
  user: {
    id: string;
    email: string;
    name?: string;
  };
  jwtToken: string;
}

export async function getSession(): Promise<Session | null> {
  if (typeof window !== 'undefined') {
    const sessionData = localStorage.getItem('userSession');
    if (sessionData) {
      try {
        const userData = JSON.parse(sessionData);
        return {
          user: {
            id: userData.user?.id || userData.id,
            email: userData.user?.email || userData.email,
            name: userData.user?.name || userData.name,
          },
          jwtToken: userData.jwtToken || userData.user?.jwtToken || '',
        };
      } catch (error) {
        console.error('Error parsing session data:', error);
        return null;
      }
    }
  }
  return null;
}

export async function signIn(email: string, password: string): Promise<{ user: any; error: any }> {
  try {
    // Use the proper login endpoint to authenticate user and get their profile
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${baseUrl}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (!response.ok) {
      let errorData: { [key: string]: any } = {};

      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, create a generic error object
        errorData = { detail: 'Invalid email or password. Please try again.' };
      }

      // Provide more specific error messages based on the backend response
      if (response.status === 401) {
        return { user: null, error: 'Invalid email or password. Please try again.' };
      } else if (response.status === 422) {
        return { user: null, error: 'Please enter a valid email and password.' };
      } else {
        return { user: null, error: errorData.detail || 'Login failed. Please check your email and password.' };
      }
    }

    const data = await response.json();

    // Now fetch the user's profile to get their actual name from the database
    const profileResponse = await fetch(`${baseUrl}/api/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${data.access_token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!profileResponse.ok) {
      // If profile fetch fails, use the token data we have
      const user = {
        id: data.user_id || `user_${email.replace('@', '_at_').replace('.', '_dot_')}`,
        email,
        name: email.split('@')[0], // fallback to email-derived name
      };

      const session = {
        user,
        jwtToken: data.access_token,
      };

      // Store session in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('userSession', JSON.stringify(session));
      }

      return { user: session.user, error: null };
    }

    const profileData = await profileResponse.json();

    const user = {
      id: profileData.id,
      email: profileData.email,
      name: profileData.name,
    };

    const session = {
      user,
      jwtToken: data.access_token,
    };

    // Store session in localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('userSession', JSON.stringify(session));
    }

    return { user: session.user, error: null };
  } catch (error) {
    console.error('Sign in error:', error);
    return { user: null, error: 'An error occurred during login. Please try again.' };
  }
}

export async function signUp(name: string, email: string, password: string): Promise<{ user: any; error: any }> {
  try {
    // Use the proper registration endpoint to create user
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${baseUrl}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        name: name,
        password: password,
        password_confirm: password, // assuming same password for confirmation
      }),
    });

    if (!response.ok) {
      let errorData: { [key: string]: any } = {};

      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, create a generic error object
        errorData = { detail: 'Registration failed. Please check your information and try again.' };
      }

      // Provide more specific error messages based on the backend response
      if (response.status === 409) {
        return { user: null, error: 'A user with this email already exists. Please use a different email or try logging in.' };
      } else if (response.status === 422) {
        return { user: null, error: 'Invalid input. Please check your email, name, and password.' };
      } else {
        return { user: null, error: errorData.detail || 'Registration failed. Please check your information and try again.' };
      }
    }

    const data = await response.json();

    // Now login to get the token
    const loginResponse = await fetch(`${baseUrl}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (!loginResponse.ok) {
      let errorData: { [key: string]: any } = {};

      try {
        errorData = await loginResponse.json();
      } catch (e) {
        // If response is not JSON, create a generic error object
        errorData = { detail: 'Registration was successful but login failed. Please try logging in manually.' };
      }

      // Handle login errors after registration
      if (loginResponse.status === 401) {
        return { user: null, error: 'Registration was successful but login failed. Please try logging in manually.' };
      } else {
        return { user: null, error: errorData.detail || 'Registration was successful but login failed. Please try logging in manually.' };
      }
    }

    const loginData = await loginResponse.json();

    const user = {
      id: data.id,
      email: data.email,
      name: data.name,
    };

    const session = {
      user,
      jwtToken: loginData.access_token,
    };

    // Store session in localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('userSession', JSON.stringify(session));
    }

    return { user: session.user, error: null };
  } catch (error) {
    console.error('Sign up error:', error);
    return { user: null, error: 'An error occurred during registration. Please try again.' };
  }
}

export async function signOut(): Promise<void> {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('userSession');
  }
}
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import ChatsPage from './components/ChatsPage';
import { AuthProvider } from "./context/auth";
import { UserProvider } from "./context/user";
import TopNav from "./components/TopNav";
import { useAuth } from './hooks';
import Login from './components/Login';
import Profile from './components/Profile';
import Registration from './components/Registration';
import Home from './components/Home';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function ErrorPage() {
  return (
    <>
      <h1>an error has occurred</h1>
      <p>contact site admin for support</p>
    </>
  );
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/chats" />} />
      <Route path="/chats" element={<ChatsPage />} />
      <Route path="/chats/:chatId" element={<ChatsPage />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main>
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <div>
              <Header />
              <Main />
            </div>
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App

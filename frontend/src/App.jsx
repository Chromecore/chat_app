import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
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
  return <h1>
    404: not found
  </h1>;
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
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-zinc-800 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <div className={className}>
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

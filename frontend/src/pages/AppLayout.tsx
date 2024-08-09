import {
  CircleUser,
  Home,
  Bot,
  BookCheck,
  Languages,
  Menu,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { NavLink, Outlet } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTrigger,
} from "@/components/ui/sheet";
import React from "react";
import { useAuth } from "@/contexts/auth";

type Route = {
  name: string;
  icon: any;
  url: string;
};

const routes: Route[] = [
  { name: "home", icon: Home, url: "home" },
  { name: "chat", icon: Bot, url: "bot" },
  { name: "scores", icon: BookCheck, url: "scores" },
];

const NavigationRoutes: React.FC = () => {
  return (
    <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
      {routes.map((route) => {
        return (
          <NavLink
            key={route.name}
            to={route.url}
            className={({ isActive }) => {
              return isActive
                ? "flex items-center gap-3 rounded-lg bg-muted px-3 py-2 text-primary transition-all hover:text-primary"
                : "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary";
            }}
          >
            <route.icon className="h-4 w-4" />
            <span className="capitalize">{route.name}</span>
          </NavLink>
        );
      })}
    </nav>
  );
};

const AppLayout: React.FC = () => {
  const { logout } = useAuth();

  return (
    <>
      <div className="grid h-screen w-screen md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr] overflow-hidden">
        <div className="hidden border-r bg-muted/40 md:block">
          <div className="flex h-full max-h-screen flex-col gap-2">
            <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
              <NavLink
                to="home"
                className="flex items-center gap-2 font-semibold"
              >
                <Languages className="h-6 w-6" />
                <span className="">Engleasy</span>
              </NavLink>
            </div>
            <div className="flex-1">
              <NavigationRoutes />
            </div>
            <div className="mt-auto p-4"></div>
          </div>
        </div>
        <div className="flex flex-col">
          <header className="flex h-14 items-center gap-4 border-b bg-muted/40 px-4 lg:h-[60px] lg:px-6">
            <Sheet>
              <SheetHeader></SheetHeader>
              <SheetTrigger asChild>
                <Button
                  variant="outline"
                  size="icon"
                  className="shrink-0 md:hidden"
                >
                  <Menu className="h-5 w-5" />
                  <span className="sr-only">Toggle navigation menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="flex flex-col">
                <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
                  <NavLink
                    to="home"
                    className="flex items-center gap-2 font-semibold"
                  >
                    <Languages className="h-6 w-6" />
                    <span className="">Engleasy</span>
                  </NavLink>
                </div>
                <div className="flex-1">
                  <NavigationRoutes />
                </div>
              </SheetContent>
            </Sheet>
            <div className="w-full flex-1"></div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="secondary" className="rounded-full">
                  <CircleUser className="h-5 w-5" />
                  <span className="sr-only">Toggle user menu</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuItem>Support</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => logout()}>
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </header>
          <main className="p-4 lg:p-6 max-w-screen-lg w-full m-auto overflow-y-scroll h-[calc(100vh-3.5rem)] lg:h-[calc(100vh-60px)] no-scrollbar">
            <Outlet />
          </main>
        </div>
      </div>
    </>
  );
};

export default AppLayout;

import React, { ReactNode } from 'react';
import ServerLayout from './serverLayout';
import ClientLayout from './clientLayout';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <ServerLayout>
      <ClientLayout>
        {children}
      </ClientLayout>
    </ServerLayout>
  );
};

export default Layout;

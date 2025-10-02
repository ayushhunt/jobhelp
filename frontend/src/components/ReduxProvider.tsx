'use client'

import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import { store, persistor } from '@/redux/store'
import Loader from './Loader'

interface ReduxProviderProps {
  children: React.ReactNode
}

export const ReduxProvider = ({ children }: ReduxProviderProps) => {
  return (
    <Provider store={store}>
      <PersistGate loading={<div className="min-h-screen flex items-center justify-center"><Loader /></div>} persistor={persistor}>
        {children}
      </PersistGate>
    </Provider>
  )
}



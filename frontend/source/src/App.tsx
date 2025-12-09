import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { GameHUD } from './components/game';
import { HomeScene } from './scenes';
import { SceneTransitionProvider } from './contexts';
import { SceneTransitionUI } from './components/common';

function App() {
    return (
        <BrowserRouter>
            <SceneTransitionProvider>
                {/* 1. UI Transition (Màn che) - Luôn nằm trên cùng */}
                <SceneTransitionUI />

                {/* 2. HUD Game - Nằm dưới màn che, trên Scene */}
                <GameHUD onOpenInventory={() => console.log('Mở túi đồ')} />

                {/* 3. Các Scene game */}
                <Routes>
                    <Route path="/" element={<HomeScene />} />
                </Routes>
            </SceneTransitionProvider>
        </BrowserRouter>
    );
}

export default App;

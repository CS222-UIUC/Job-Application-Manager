import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage.jsx';
import Login from './Login.jsx';
import TrackerMain from './TrackerMain.jsx';

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<HomePage />} />
				<Route path="/login" element={<Login />} />
				<Route path="/tracker" element={<TrackerMain />} />
			</Routes>
		</BrowserRouter>
	);
}

export default App

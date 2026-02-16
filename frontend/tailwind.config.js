/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                ibm: {
                    blue: {
                        10: '#f4f7fb', // Light background
                        20: '#e0e6ed', // Border
                        50: '#0f62fe', // Primary Blue
                        60: '#0043ce', // Hover Blue
                        80: '#002d9c', // Dark Blue
                        90: '#001d6c', // Very Dark Blue
                    },
                    gray: {
                        10: '#f4f4f4',
                        80: '#393939',
                        100: '#161616', // Dark background
                    }
                }
            },
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui'],
            }
        },
    },
    plugins: [],
}

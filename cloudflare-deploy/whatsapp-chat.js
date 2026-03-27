// Enhanced WhatsApp Chat Integration

// WhatsApp Configuration
const WHATSAPP_CONFIG = {
    phoneNumber: '8619879476613',
    businessHours: {
        start: 9, // 9 AM
        end: 18   // 6 PM
    },
    timezone: 'Asia/Shanghai',
    quickMessages: [
        {
            label: 'Get Price Quote',
            message: 'Hello, I would like to get a price quote for crystal products.'
        },
        {
            label: 'Request Catalog',
            message: 'Hi, could you send me the complete product catalog?'
        },
        {
            label: 'Order Samples',
            message: 'Hello, I want to request free samples to test quality.'
        },
        {
            label: 'Custom Design',
            message: 'Hi, I need a custom crystal design for my project.'
        },
        {
            label: 'General Inquiry',
            message: 'Hello, I have some questions about your crystal products.'
        }
    ]
};

// Check if business hours
function isBusinessHours() {
    const now = new Date();
    const hour = now.getHours();
    return hour >= WHATSAPP_CONFIG.businessHours.start &&
           hour < WHATSAPP_CONFIG.businessHours.end;
}

// Create WhatsApp Chat Widget
function createWhatsAppChat() {
    // Check if widget already exists
    if (document.getElementById('whatsapp-widget')) {
        return;
    }

    // Create widget container
    const widget = document.createElement('div');
    widget.id = 'whatsapp-widget';
    widget.innerHTML = `
        <style>
            #whatsapp-widget {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 9999;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }

            .whatsapp-float {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 5px 20px rgba(37, 211, 102, 0.4);
                transition: all 0.3s ease;
                text-decoration: none;
                position: relative;
            }

            .whatsapp-float:hover {
                transform: scale(1.1);
                box-shadow: 0 8px 30px rgba(37, 211, 102, 0.6);
            }

            .whatsapp-float svg {
                width: 35px;
                height: 35px;
                fill: white;
            }

            .whatsapp-status {
                position: absolute;
                top: -5px;
                right: -5px;
                width: 18px;
                height: 18px;
                background: #25d366;
                border: 3px solid white;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(37, 211, 102, 0); }
                100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
            }

            .whatsapp-popup {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 300px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                overflow: hidden;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
                visibility: hidden;
            }

            .whatsapp-popup.active {
                opacity: 1;
                transform: translateY(0);
                visibility: visible;
            }

            .whatsapp-popup-header {
                background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }

            .whatsapp-popup-header h4 {
                margin: 0 0 5px 0;
                font-size: 18px;
            }

            .whatsapp-popup-header p {
                margin: 0;
                font-size: 13px;
                opacity: 0.9;
            }

            .whatsapp-popup-body {
                padding: 20px;
            }

            .quick-message-btn {
                display: block;
                width: 100%;
                padding: 12px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 14px;
                color: #333;
                font-weight: 500;
            }

            .quick-message-btn:hover {
                background: #25d366;
                border-color: #25d366;
                color: white;
                transform: translateY(-2px);
            }

            .whatsapp-popup-footer {
                padding: 15px 20px;
                background: #f8f9fa;
                text-align: center;
                border-top: 1px solid #e9ecef;
            }

            .whatsapp-popup-footer p {
                margin: 0;
                font-size: 12px;
                color: #666;
            }

            .whatsapp-badge {
                position: absolute;
                top: 0;
                left: 0;
                background: #e53935;
                color: white;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                font-weight: bold;
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .whatsapp-float {
                    width: 55px;
                    height: 55px;
                    bottom: 20px;
                    right: 20px;
                }

                .whatsapp-float svg {
                    width: 30px;
                    height: 30px;
                }

                .whatsapp-popup {
                    width: 280px;
                    right: -100px;
                }

                .quick-message-btn {
                    padding: 10px;
                    font-size: 13px;
                }
            }
        </style>

        <div class="whatsapp-float" id="whatsapp-float-btn">
            <div class="whatsapp-status" id="whatsapp-status"></div>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8-5.7-9.8-14.5-5.5-2.9 2.8-11.4 12.5-14 14-2.6 1.6-5.1 2.3-8.7-.1-12.1-2.8-31.4-15.5-68.1-34.1-45.1-26.9-77.5-57.5-111-109.6-3.2-4.9-5.9-5.7-8.6-5.7-2.6 0-5.3 0-8.1 0-2.8 0-7.4 1-11.3 5.3-3.9 4.2-15.1 14.8-15.1 36.1 0 21.3 15.5 41.9 17.6 46.5 2.1 4.6 30.2 46.1 73.2 72.5 10.2 6.1 18.2 9.7 24.4 12.5 10.9 4.6 20.8 4 28.6 2.4 8.8-1.8 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-9.9-10.7-19.3z"/>
            </svg>
            <div class="whatsapp-badge" id="whatsapp-badge">1</div>
        </div>

        <div class="whatsapp-popup" id="whatsapp-popup">
            <div class="whatsapp-popup-header">
                <h4>💬 Chat with Us</h4>
                <p id="whatsapp-hours-status">We're online! Response in 2 hours</p>
            </div>
            <div class="whatsapp-popup-body" id="quick-messages-container">
                <!-- Quick messages will be added here -->
            </div>
            <div class="whatsapp-popup-footer">
                <p>⚡ Typical response: 2 hours during business hours</p>
            </div>
        </div>
    `;

    document.body.appendChild(widget);

    // Add quick messages
    const quickMessagesContainer = document.getElementById('quick-messages-container');
    WHATSAPP_CONFIG.quickMessages.forEach(msg => {
        const btn = document.createElement('a');
        btn.className = 'quick-message-btn';
        btn.textContent = msg.label;
        btn.href = `https://wa.me/${WHATSAPP_CONFIG.phoneNumber}?text=${encodeURIComponent(msg.message)}`;
        btn.target = '_blank';
        quickMessagesContainer.appendChild(btn);
    });

    // Update business hours status
    updateWhatsAppStatus();

    // Add event listeners
    const floatBtn = document.getElementById('whatsapp-float-btn');
    const popup = document.getElementById('whatsapp-popup');

    floatBtn.addEventListener('click', (e) => {
        e.preventDefault();
        popup.classList.toggle('active');

        // Hide badge on first click
        const badge = document.getElementById('whatsapp-badge');
        if (badge) {
            badge.style.display = 'none';
        }
    });

    // Close popup when clicking outside
    document.addEventListener('click', (e) => {
        if (!widget.contains(e.target)) {
            popup.classList.remove('active');
        }
    });
}

// Update WhatsApp status
function updateWhatsAppStatus() {
    const isOnline = isBusinessHours();
    const statusText = document.getElementById('whatsapp-hours-status');
    const statusIndicator = document.getElementById('whatsapp-status');

    if (statusText) {
        if (isOnline) {
            statusText.textContent = "🟢 We're online! Response in 2 hours";
            statusText.style.color = '#25d366';
        } else {
            statusText.textContent = "⚪ Offline. Leave a message, we'll reply ASAP";
            statusText.style.color = '#666';
        }
    }

    if (statusIndicator) {
        if (isOnline) {
            statusIndicator.style.background = '#25d366';
            statusIndicator.style.animation = 'pulse 2s infinite';
        } else {
            statusIndicator.style.background = '#999';
            statusIndicator.style.animation = 'none';
        }
    }
}

// Initialize WhatsApp Chat
document.addEventListener('DOMContentLoaded', () => {
    // Wait for page to load
    setTimeout(() => {
        createWhatsAppChat();
    }, 1000);

    // Update status every minute
    setInterval(updateWhatsAppStatus, 60000);
});

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createWhatsAppChat,
        updateWhatsAppStatus,
        isBusinessHours
    };
}

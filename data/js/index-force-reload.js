// Khắc phục vấn đề cache - tự động cập nhật dữ liệu mới
document.addEventListener('DOMContentLoaded', function() {
    
    // Force reload tất cả CSS và JS files với timestamp
    function addTimestampToAssets() {
        const timestamp = new Date().getTime();
        
        // Cập nhật CSS files
        const cssLinks = document.querySelectorAll('link[rel="stylesheet"]');
        cssLinks.forEach(link => {
            const href = link.href;
            const separator = href.includes('?') ? '&' : '?';
            link.href = href.split('?')[0] + separator + 'v=' + timestamp;
        });
        
        // Cập nhật JS files (trừ file hiện tại)
        const scripts = document.querySelectorAll('script[src]');
        scripts.forEach(script => {
            const src = script.src;
            if (src && !src.includes('index.js')) {
                const separator = src.includes('?') ? '&' : '?';
                script.src = src.split('?')[0] + separator + 'v=' + timestamp;
            }
        });
    }
    
    // Disable cache cho các AJAX requests
    function disableAjaxCache() {
        // Nếu sử dụng jQuery
        if (typeof $ !== 'undefined') {
            $.ajaxSetup({
                cache: false,
                beforeSend: function(xhr, settings) {
                    const separator = settings.url.includes('?') ? '&' : '?';
                    settings.url += separator + '_=' + new Date().getTime();
                }
            });
        }
        
        // Override fetch để thêm timestamp
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (typeof url === 'string') {
                const separator = url.includes('?') ? '&' : '?';
                url += separator + '_=' + new Date().getTime();
            }
            
            // Thêm headers để disable cache
            options.headers = {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0',
                ...options.headers
            };
            
            return originalFetch(url, options);
        };
    }
    
    // Set meta tags để disable cache
    function setNoCacheHeaders() {
        // Tạo hoặc cập nhật meta tags
        const metaTags = [
            { name: 'cache-control', content: 'no-cache, no-store, must-revalidate' },
            { name: 'pragma', content: 'no-cache' },
            { name: 'expires', content: '0' }
        ];
        
        metaTags.forEach(tag => {
            let meta = document.querySelector(`meta[http-equiv="${tag.name}"]`);
            if (!meta) {
                meta = document.createElement('meta');
                meta.setAttribute('http-equiv', tag.name);
                document.head.appendChild(meta);
            }
            meta.setAttribute('content', tag.content);
        });
    }
    
    // Auto refresh page nếu có thay đổi (optional)
    function setupAutoRefresh() {
        // Check server mỗi 30 giây để xem có cập nhật không
        let lastModified = document.lastModified;
        
        setInterval(() => {
            fetch(window.location.href, {
                method: 'HEAD',
                cache: 'no-cache'
            })
            .then(response => {
                const newLastModified = response.headers.get('last-modified');
                if (newLastModified && newLastModified !== lastModified) {
                    console.log('Phát hiện cập nhật mới, đang tải lại trang...');
                    window.location.reload(true);
                }
            })
            .catch(err => console.log('Auto refresh check failed:', err));
        }, 30000); // Check mỗi 30 giây
    }
    
    // Khởi chạy các function
    setNoCacheHeaders();
    disableAjaxCache();
    
    // Uncomment dòng dưới nếu muốn auto refresh
    // setupAutoRefresh();
    
    // Force reload assets khi cần thiết
    if (performance.navigation.type !== performance.navigation.TYPE_RELOAD) {
        addTimestampToAssets();
    }
    
    console.log('Cache prevention đã được kích hoạt');
});

// Thêm shortcut để force refresh dễ dàng
document.addEventListener('keydown', function(e) {
    // Ctrl + Shift + R để force reload
    if (e.ctrlKey && e.shiftKey && e.key === 'R') {
        e.preventDefault();
        window.location.reload(true);
    }
});

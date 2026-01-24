// vite.config.js
import { defineConfig } from "file:///C:/Users/mamta/Downloads/kaizer-main/kaizer-main/frontend/node_modules/vite/dist/node/index.js";
import react from "file:///C:/Users/mamta/Downloads/kaizer-main/kaizer-main/frontend/node_modules/@vitejs/plugin-react/dist/index.mjs";
import tailwindcss from "file:///C:/Users/mamta/Downloads/kaizer-main/kaizer-main/frontend/node_modules/@tailwindcss/vite/dist/index.mjs";
var vite_config_default = defineConfig({
  plugins: [
    react(),
    tailwindcss()
    //,
    // visualizer({
    //   template: 'treemap', // or sunburst
    //   open: true,
    //   gzipSize: true,
    //   brotliSize: true,
    //   filename: 'stats.html', // analysis file
    // }),
  ],
  server: {
    port: 3e3,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8127",
        changeOrigin: true,
        ws: true,
        configure: (proxy, options) => {
          proxy.on("open", (proxySocket) => {
            console.log("[WS Proxy] Connection opened");
          });
          proxy.on("close", (res, socket, head) => {
            console.log("[WS Proxy] Connection closed");
          });
          proxy.on("proxyReq", (proxyReq, req) => {
            console.log(`[Proxy] Redirecting: ${req.method} ${req.url}`);
          });
          proxy.on("error", (err, req, res) => {
            console.error(`[Proxy] Error on ${req.method} ${req.url}: ${err.message}`);
            if (res && !res.headersSent) {
              res.writeHead(500, { "Content-Type": "text/plain" });
              res.end("Proxy error: " + err.message);
            } else if (res) {
              res.end();
            }
          });
        }
      }
    }
  },
  build: {
    sourcemap: false
    // Explicitly enable sourcemaps for builds
    /*rollupOptions: {
      output: {
        manualChunks(id) {
          // This creates a separate chunk for each node module, which is useful for debugging bundle sizes.
          if (id.includes('node_modules')) {
            const packageNameMatch = id.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/);
            if (packageNameMatch) {
              const packageName = packageNameMatch[1];
              // Create a chunk for each package.
              // e.g. @mantine/core -> vendor-mantine-core
              return `vendor-${packageName.replace('@', '').replace('/', '-')}`;
            }
          }
        },
        //manualChunks: {
        //  plotly: ['react-plotly.js', 'plotly.js'],
        //  stringToReactComponent: ['string-to-react-component'],
        //},
      },
    },*/
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxtYW10YVxcXFxEb3dubG9hZHNcXFxca2FpemVyLW1haW5cXFxca2FpemVyLW1haW5cXFxcZnJvbnRlbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXG1hbXRhXFxcXERvd25sb2Fkc1xcXFxrYWl6ZXItbWFpblxcXFxrYWl6ZXItbWFpblxcXFxmcm9udGVuZFxcXFx2aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovVXNlcnMvbWFtdGEvRG93bmxvYWRzL2thaXplci1tYWluL2thaXplci1tYWluL2Zyb250ZW5kL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSdcbmltcG9ydCByZWFjdCBmcm9tICdAdml0ZWpzL3BsdWdpbi1yZWFjdCdcbmltcG9ydCB0YWlsd2luZGNzcyBmcm9tICdAdGFpbHdpbmRjc3Mvdml0ZSdcbmltcG9ydCB7IEJ1ZmZlciB9IGZyb20gJ2J1ZmZlcic7XG4vL2ltcG9ydCB7IHZpc3VhbGl6ZXIgfSBmcm9tICdyb2xsdXAtcGx1Z2luLXZpc3VhbGl6ZXInO1xuXG4vLyBodHRwczovL3ZpdGUuZGV2L2NvbmZpZy9cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIHBsdWdpbnM6IFtcbiAgICAgIHJlYWN0KCksXG4gICAgICB0YWlsd2luZGNzcygpLy8sXG4gICAgIC8vIHZpc3VhbGl6ZXIoe1xuICAgICAvLyAgIHRlbXBsYXRlOiAndHJlZW1hcCcsIC8vIG9yIHN1bmJ1cnN0XG4gICAgIC8vICAgb3BlbjogdHJ1ZSxcbiAgICAgLy8gICBnemlwU2l6ZTogdHJ1ZSxcbiAgICAgLy8gICBicm90bGlTaXplOiB0cnVlLFxuICAgICAvLyAgIGZpbGVuYW1lOiAnc3RhdHMuaHRtbCcsIC8vIGFuYWx5c2lzIGZpbGVcbiAgICAgLy8gfSksXG4gIF0sXG4gIHNlcnZlcjoge1xuICAgIHBvcnQ6IDMwMDAsXG4gICAgcHJveHk6IHtcbiAgICAgICcvYXBpJzoge1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vMTI3LjAuMC4xOjgxMjcnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgIFxuICAgICAgICB3czogdHJ1ZSxcblxuXG4gICAgICAgIGNvbmZpZ3VyZTogKHByb3h5LCBvcHRpb25zKSA9PiB7XG5cbiAgICAgICAgICAgIFxuICAgICAgICAgIHByb3h5Lm9uKCdvcGVuJywgKHByb3h5U29ja2V0KSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmxvZygnW1dTIFByb3h5XSBDb25uZWN0aW9uIG9wZW5lZCcpO1xuICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgcHJveHkub24oJ2Nsb3NlJywgKHJlcywgc29ja2V0LCBoZWFkKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmxvZygnW1dTIFByb3h5XSBDb25uZWN0aW9uIGNsb3NlZCcpO1xuICAgICAgICAgIH0pO1xuXG5cblxuICAgICAgICAgIHByb3h5Lm9uKCdwcm94eVJlcScsIChwcm94eVJlcSwgcmVxKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhgW1Byb3h5XSBSZWRpcmVjdGluZzogJHtyZXEubWV0aG9kfSAke3JlcS51cmx9YCk7XG4gICAgICAgICAgfSk7XG5cbiAgICAgICAgICAvKnByb3h5Lm9uKCdwcm94eVJlcycsIChwcm94eVJlcywgcmVxKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBjaHVua3MgPSBbXTtcblxuICAgICAgICAgICAgcHJveHlSZXMub24oJ2RhdGEnLCAoY2h1bmspID0+IHtcbiAgICAgICAgICAgICAgY2h1bmtzLnB1c2goY2h1bmspO1xuICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgIHByb3h5UmVzLm9uKCdlbmQnLCAoKSA9PiB7XG4gICAgICAgICAgICAgIGNvbnN0IGJvZHkgPSBCdWZmZXIuY29uY2F0KGNodW5rcykudG9TdHJpbmcoJ3V0ZjgnKTtcblxuICAgICAgICAgICAgICBpZiAoYm9keS50cmltKCkubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGBbUHJveHldIFJlc3BvbnNlIGZvciAke3JlcS5tZXRob2R9ICR7cmVxLnVybH06YCk7XG4gICAgICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgICAgIGNvbnN0IHBhcnNlZCA9IEpTT04ucGFyc2UoYm9keSk7XG4gICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhKU09OLnN0cmluZ2lmeShwYXJzZWQsIG51bGwsIDIpKTtcbiAgICAgICAgICAgICAgICB9IGNhdGNoIHtcbiAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGJvZHkpOyAvLyBGYWxsYmFjayBpZiBub3QgSlNPTlxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfSk7XG4gICAgICAgICAgKi9cblxuICAgICAgICAgIHByb3h5Lm9uKCdlcnJvcicsIChlcnIsIHJlcSwgcmVzKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmVycm9yKGBbUHJveHldIEVycm9yIG9uICR7cmVxLm1ldGhvZH0gJHtyZXEudXJsfTogJHtlcnIubWVzc2FnZX1gKTtcbiAgICAgICAgICAgIGlmIChyZXMgJiYgIXJlcy5oZWFkZXJzU2VudCkge1xuICAgICAgICAgICAgICByZXMud3JpdGVIZWFkKDUwMCwgeyAnQ29udGVudC1UeXBlJzogJ3RleHQvcGxhaW4nIH0pO1xuICAgICAgICAgICAgICByZXMuZW5kKCdQcm94eSBlcnJvcjogJyArIGVyci5tZXNzYWdlKTtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAocmVzKSB7XG4gICAgICAgICAgICAgIHJlcy5lbmQoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9KTtcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSxcbiAgfSxcbiAgYnVpbGQ6IHtcbiAgICBzb3VyY2VtYXA6IGZhbHNlLCAvLyBFeHBsaWNpdGx5IGVuYWJsZSBzb3VyY2VtYXBzIGZvciBidWlsZHNcbiAgICAvKnJvbGx1cE9wdGlvbnM6IHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBtYW51YWxDaHVua3MoaWQpIHtcbiAgICAgICAgICAvLyBUaGlzIGNyZWF0ZXMgYSBzZXBhcmF0ZSBjaHVuayBmb3IgZWFjaCBub2RlIG1vZHVsZSwgd2hpY2ggaXMgdXNlZnVsIGZvciBkZWJ1Z2dpbmcgYnVuZGxlIHNpemVzLlxuICAgICAgICAgIGlmIChpZC5pbmNsdWRlcygnbm9kZV9tb2R1bGVzJykpIHtcbiAgICAgICAgICAgIGNvbnN0IHBhY2thZ2VOYW1lTWF0Y2ggPSBpZC5tYXRjaCgvW1xcXFwvXW5vZGVfbW9kdWxlc1tcXFxcL10oLio/KShbXFxcXC9dfCQpLyk7XG4gICAgICAgICAgICBpZiAocGFja2FnZU5hbWVNYXRjaCkge1xuICAgICAgICAgICAgICBjb25zdCBwYWNrYWdlTmFtZSA9IHBhY2thZ2VOYW1lTWF0Y2hbMV07XG4gICAgICAgICAgICAgIC8vIENyZWF0ZSBhIGNodW5rIGZvciBlYWNoIHBhY2thZ2UuXG4gICAgICAgICAgICAgIC8vIGUuZy4gQG1hbnRpbmUvY29yZSAtPiB2ZW5kb3ItbWFudGluZS1jb3JlXG4gICAgICAgICAgICAgIHJldHVybiBgdmVuZG9yLSR7cGFja2FnZU5hbWUucmVwbGFjZSgnQCcsICcnKS5yZXBsYWNlKCcvJywgJy0nKX1gO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgLy9tYW51YWxDaHVua3M6IHtcbiAgICAgICAgLy8gIHBsb3RseTogWydyZWFjdC1wbG90bHkuanMnLCAncGxvdGx5LmpzJ10sXG4gICAgICAgIC8vICBzdHJpbmdUb1JlYWN0Q29tcG9uZW50OiBbJ3N0cmluZy10by1yZWFjdC1jb21wb25lbnQnXSxcbiAgICAgICAgLy99LFxuICAgICAgfSxcbiAgICB9LCovXG4gIH1cbn0pXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQTJXLFNBQVMsb0JBQW9CO0FBQ3hZLE9BQU8sV0FBVztBQUNsQixPQUFPLGlCQUFpQjtBQUt4QixJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTO0FBQUEsSUFDTCxNQUFNO0FBQUEsSUFDTixZQUFZO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLEVBUWhCO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixPQUFPO0FBQUEsTUFDTCxRQUFRO0FBQUEsUUFDTixRQUFRO0FBQUEsUUFDUixjQUFjO0FBQUEsUUFFZCxJQUFJO0FBQUEsUUFHSixXQUFXLENBQUMsT0FBTyxZQUFZO0FBRzdCLGdCQUFNLEdBQUcsUUFBUSxDQUFDLGdCQUFnQjtBQUNoQyxvQkFBUSxJQUFJLDhCQUE4QjtBQUFBLFVBQzVDLENBQUM7QUFFRCxnQkFBTSxHQUFHLFNBQVMsQ0FBQyxLQUFLLFFBQVEsU0FBUztBQUN2QyxvQkFBUSxJQUFJLDhCQUE4QjtBQUFBLFVBQzVDLENBQUM7QUFJRCxnQkFBTSxHQUFHLFlBQVksQ0FBQyxVQUFVLFFBQVE7QUFDdEMsb0JBQVEsSUFBSSx3QkFBd0IsSUFBSSxNQUFNLElBQUksSUFBSSxHQUFHLEVBQUU7QUFBQSxVQUM3RCxDQUFDO0FBeUJELGdCQUFNLEdBQUcsU0FBUyxDQUFDLEtBQUssS0FBSyxRQUFRO0FBQ25DLG9CQUFRLE1BQU0sb0JBQW9CLElBQUksTUFBTSxJQUFJLElBQUksR0FBRyxLQUFLLElBQUksT0FBTyxFQUFFO0FBQ3pFLGdCQUFJLE9BQU8sQ0FBQyxJQUFJLGFBQWE7QUFDM0Isa0JBQUksVUFBVSxLQUFLLEVBQUUsZ0JBQWdCLGFBQWEsQ0FBQztBQUNuRCxrQkFBSSxJQUFJLGtCQUFrQixJQUFJLE9BQU87QUFBQSxZQUN2QyxXQUFXLEtBQUs7QUFDZCxrQkFBSSxJQUFJO0FBQUEsWUFDVjtBQUFBLFVBQ0YsQ0FBQztBQUFBLFFBQ0g7QUFBQSxNQUNGO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFBQSxFQUNBLE9BQU87QUFBQSxJQUNMLFdBQVc7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQSxFQXFCYjtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==

        // ==================== 數據導出功能 ====================
        
        // 清除導出日期
        function clearExportDates() {
            document.getElementById('export-start-date').value = '';
            document.getElementById('export-end-date').value = '';
        }
        
        // 設置今天範圍
        function setTodayRange() {
            const today = new Date();
            const startOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
            const endOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59);
            
            document.getElementById('export-start-date').value = formatDateTimeLocal(startOfDay);
            document.getElementById('export-end-date').value = formatDateTimeLocal(endOfDay);
        }
        
        // 設置本週範圍
        function setWeekRange() {
            const today = new Date();
            const dayOfWeek = today.getDay();
            const startOfWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - dayOfWeek);
            const endOfWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() + (6 - dayOfWeek), 23, 59, 59);
            
            document.getElementById('export-start-date').value = formatDateTimeLocal(startOfWeek);
            document.getElementById('export-end-date').value = formatDateTimeLocal(endOfWeek);
        }
        
        // 設置本月範圍
        function setMonthRange() {
            const today = new Date();
            const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
            const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0, 23, 59, 59);
            
            document.getElementById('export-start-date').value = formatDateTimeLocal(startOfMonth);
            document.getElementById('export-end-date').value = formatDateTimeLocal(endOfMonth);
        }
        
        // 格式化日期時間為本地格式
        function formatDateTimeLocal(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            
            return `${year}-${month}-${day}T${hours}:${minutes}`;
        }
        
        // 清除篩選範圍內的數據
        async function clearFilteredData() {
            const startDate = document.getElementById('export-start-date').value;
            const endDate = document.getElementById('export-end-date').value;
            
            if (!startDate && !endDate) {
                alert('請選擇要清除的日期範圍');
                return;
            }
            
            const dateRange = startDate && endDate ? 
                `${startDate} 至 ${endDate}` : 
                startDate ? `${startDate} 之後` : `${endDate} 之前`;
            
            if (!confirm(`確定要清除 ${dateRange} 的數據嗎？此操作無法撤銷。`)) {
                return;
            }
            
            try {
                const response = await fetch('/api/admin/clear_data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        start_date: startDate || null,
                        end_date: endDate || null
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    alert('數據清除成功');
                    loadDetailedStats();
                    loadAdminStats();
                } else {
                    alert('數據清除失敗');
                }
            } catch (error) {
                console.error('清除數據失敗:', error);
                alert('清除數據失敗，請重試');
            }
        }
        
        // 導出Excel
        async function exportExcel() {
            const startDate = document.getElementById('export-start-date').value;
            const endDate = document.getElementById('export-end-date').value;
            
            // 顯示載入狀態
            document.getElementById('excel-loading').style.display = 'inline';
            document.getElementById('excel-text').style.display = 'none';
            
            try {
                const response = await fetch('/api/admin/export/excel', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        start_date: startDate || null,
                        end_date: endDate || null
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    // 創建下載鏈接
                    const link = document.createElement('a');
                    link.href = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + result.data;
                    link.download = result.filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    alert('Excel文件導出成功！');
                } else {
                    alert('Excel導出失敗：' + result.error);
                }
            } catch (error) {
                console.error('Excel導出失敗:', error);
                alert('Excel導出失敗，請重試');
            } finally {
                // 恢復按鈕狀態
                document.getElementById('excel-loading').style.display = 'none';
                document.getElementById('excel-text').style.display = 'inline';
            }
        }
        
        // 導出PowerPoint
        async function exportPowerPoint() {
            const startDate = document.getElementById('export-start-date').value;
            const endDate = document.getElementById('export-end-date').value;
            
            // 顯示載入狀態
            document.getElementById('ppt-loading').style.display = 'inline';
            document.getElementById('ppt-text').style.display = 'none';
            
            try {
                const response = await fetch('/api/admin/export/powerpoint', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        start_date: startDate || null,
                        end_date: endDate || null
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    // 創建下載鏈接
                    const link = document.createElement('a');
                    link.href = 'data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,' + result.data;
                    link.download = result.filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    alert('PowerPoint文件導出成功！');
                } else {
                    alert('PowerPoint導出失敗：' + result.error);
                }
            } catch (error) {
                console.error('PowerPoint導出失敗:', error);
                alert('PowerPoint導出失敗，請重試');
            } finally {
                // 恢復按鈕狀態
                document.getElementById('ppt-loading').style.display = 'none';
                document.getElementById('ppt-text').style.display = 'inline';
            }
        }


    </script>
</body>

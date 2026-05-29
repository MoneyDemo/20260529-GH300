using System;
using System.Collections.ObjectModel;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows;
using Wpf.Ui.Appearance;
using Wpf.Ui.Controls;

namespace ParallelAsyncExample
{
    public partial class MainWindow : FluentWindow
    {
        private readonly HttpClient _client = new HttpClient { MaxResponseContentBufferSize = 1_000_000 };
        private readonly Dictionary<string, ResultItem> _resultLookup = new(StringComparer.OrdinalIgnoreCase);

        private readonly IEnumerable<string> _urlList = new string[]
        {
            "https://docs.microsoft.com",
            "https://docs.microsoft.com/azure",
            "https://docs.microsoft.com/powershell",
            "https://docs.microsoft.com/dotnet",
            "https://docs.microsoft.com/aspnet/core",
            "https://docs.microsoft.com/windows",
            "https://docs.microsoft.com/office",
            "https://docs.microsoft.com/enterprise-mobility-security",
            "https://docs.microsoft.com/visualstudio",
            "https://docs.microsoft.com/microsoft-365",
            "https://docs.microsoft.com/sql",
            "https://docs.microsoft.com/dynamics365",
            "https://docs.microsoft.com/surface",
            "https://docs.microsoft.com/xamarin",
            "https://docs.microsoft.com/azure/devops",
            "https://docs.microsoft.com/system-center",
            "https://docs.microsoft.com/graph",
            "https://docs.microsoft.com/education",
            "https://docs.microsoft.com/gaming"
        };

        public ObservableCollection<ResultItem> Results { get; } = new ObservableCollection<ResultItem>();

        public MainWindow()
        {
            InitializeComponent();

            DataContext = this;
            ApplyTheme(isDark: false);
            SetThemeToggleState();
            UpdateSummaryText("準備就緒，共 19 個 URL 可供下載。", null, null);
        }

        private void OnStartButtonClick(object sender, RoutedEventArgs e)
        {
            _startButton.IsEnabled = false;
            _progressRing.Visibility = Visibility.Visible;
            PrepareResultRows();
            UpdateSummaryText("下載已開始，正在平行處理所有 URL。", null, null);

            Task.Run(() => StartSumPageSizesAsync());
        }

        private void OnThemeToggleChanged(object sender, RoutedEventArgs e)
        {
            ApplyTheme(_themeToggleSwitch.IsChecked == true);
            SetThemeToggleState();
        }

        private async Task StartSumPageSizesAsync()
        {
            try
            {
                await SumPageSizesAsync();
            }
            finally
            {
                await Dispatcher.BeginInvoke(() =>
                {
                    _progressRing.Visibility = Visibility.Collapsed;
                    _startButton.IsEnabled = true;
                });
            }
        }

        private async Task SumPageSizesAsync()
        {
            var stopwatch = Stopwatch.StartNew();

            IEnumerable<Task<int>> downloadTasksQuery =
                from url in _urlList
                select ProcessUrlAsync(url, _client);

            Task<int>[] downloadTasks = downloadTasksQuery.ToArray();

            int[] lengths = await Task.WhenAll(downloadTasks);
            int total = lengths.Sum();

            await Dispatcher.BeginInvoke(() =>
            {
                stopwatch.Stop();

                int completedCount = Results.Count(item => item.Status == ResultStatus.CompletedText);
                int failedCount = Results.Count(item => item.Status == ResultStatus.FailedText);

                UpdateSummaryText($"下載完成，共處理 {Results.Count} 筆項目。", total, stopwatch.Elapsed, completedCount, failedCount);
            });
        }

        private async Task<int> ProcessUrlAsync(string url, HttpClient client)
        {
            await UpdateResultAsync(url, item => item.Status = ResultStatus.DownloadingText);

            try
            {
                byte[] byteArray = await client.GetByteArrayAsync(url);
                await UpdateResultAsync(url, item =>
                {
                    item.Bytes = byteArray.Length;
                    item.Status = ResultStatus.CompletedText;
                    item.ErrorMessage = string.Empty;
                });

                return byteArray.Length;
            }
            catch (Exception ex)
            {
                await UpdateResultAsync(url, item =>
                {
                    item.Bytes = null;
                    item.Status = ResultStatus.FailedText;
                    item.ErrorMessage = ex.Message;
                });

                return 0;
            }
        }

        private void PrepareResultRows()
        {
            Results.Clear();
            _resultLookup.Clear();

            foreach (string url in _urlList)
            {
                var item = new ResultItem(url)
                {
                    Status = ResultStatus.QueuedText
                };

                Results.Add(item);
                _resultLookup[url] = item;
            }
        }

        private Task UpdateResultAsync(string url, Action<ResultItem> updateAction) =>
            Dispatcher.BeginInvoke(() =>
            {
                if (_resultLookup.TryGetValue(url, out ResultItem item))
                {
                    updateAction(item);
                }
            }).Task;

        private void ApplyTheme(bool isDark)
        {
            ApplicationThemeManager.Apply(
                isDark ? ApplicationTheme.Dark : ApplicationTheme.Light,
                WindowBackdropType.Mica,
                updateAccent: true);
        }

        private void SetThemeToggleState()
        {
            bool isDark = ApplicationThemeManager.GetAppTheme() == ApplicationTheme.Dark;

            _themeToggleSwitch.IsChecked = isDark;
            _themeModeTextBlock.Text = isDark ? "深色模式" : "淺色模式";
        }

        private void UpdateSummaryText(string message, int? totalBytes, TimeSpan? elapsed, int? completedCount = null, int? failedCount = null)
        {
            string bytesPart = totalBytes.HasValue ? $"總位元組: {totalBytes.Value:#,#}" : "總位元組: -";
            string elapsedPart = elapsed.HasValue ? $"耗時: {elapsed.Value}" : "耗時: -";
            string completedPart = completedCount.HasValue ? $"完成: {completedCount.Value}" : "完成: -";
            string failedPart = failedCount.HasValue ? $"失敗: {failedCount.Value}" : "失敗: -";

            _summaryTextBlock.Text = $"{message}    {bytesPart}    {elapsedPart}    {completedPart}    {failedPart}";
        }

        protected override void OnClosed(EventArgs e)
        {
            _client.Dispose();
            base.OnClosed(e);
        }

        private static class ResultStatus
        {
            public const string QueuedText = "Queued";
            public const string DownloadingText = "Downloading";
            public const string CompletedText = "Completed";
            public const string FailedText = "Failed";
        }

        public sealed class ResultItem : INotifyPropertyChanged
        {
            private int? _bytes;
            private string _status = ResultStatus.QueuedText;
            private string _errorMessage = string.Empty;

            public ResultItem(string url)
            {
                Url = url;
            }

            public string Url { get; }

            public int? Bytes
            {
                get => _bytes;
                set
                {
                    if (_bytes == value)
                    {
                        return;
                    }

                    _bytes = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(BytesDisplay));
                }
            }

            public string BytesDisplay => Bytes.HasValue ? $"{Bytes.Value:#,#}" : "-";

            public string Status
            {
                get => _status;
                set
                {
                    if (_status == value)
                    {
                        return;
                    }

                    _status = value;
                    OnPropertyChanged();
                }
            }

            public string ErrorMessage
            {
                get => _errorMessage;
                set
                {
                    if (_errorMessage == value)
                    {
                        return;
                    }

                    _errorMessage = value;
                    OnPropertyChanged();
                }
            }

            public event PropertyChangedEventHandler PropertyChanged;

            private void OnPropertyChanged([CallerMemberName] string propertyName = null)
            {
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
}

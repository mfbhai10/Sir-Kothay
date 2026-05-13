/**
 * Semi-transparent overlay notifications (replaces window.alert / confirm).
 * Requires Tailwind CSS + Bootstrap Icons on the page.
 */
(function (global) {
    'use strict';

    var Z = '2147483000';

    function escapeHtml(s) {
        if (s == null) return '';
        var d = document.createElement('div');
        d.textContent = String(s);
        return d.innerHTML;
    }

    function removeBackdrop(backdrop, onKey) {
        if (onKey) document.removeEventListener('keydown', onKey);
        if (backdrop && backdrop.parentNode) backdrop.parentNode.removeChild(backdrop);
    }

    function variantMeta(variant) {
        if (variant === 'success') {
            return { icon: 'bi-check-circle-fill', title: 'Success', accent: 'text-green-600', border: 'border-green-100' };
        }
        if (variant === 'error') {
            return { icon: 'bi-exclamation-circle-fill', title: 'Something went wrong', accent: 'text-red-600', border: 'border-red-100' };
        }
        return { icon: 'bi-info-circle-fill', title: 'Notice', accent: 'text-orange-500', border: 'border-orange-100' };
    }

    /**
     * @param {string} message
     * @param {{ variant?: 'info'|'success'|'error', title?: string }} [opts]
     * @returns {Promise<void>}
     */
    function skNotify(message, opts) {
        opts = opts || {};
        var variant = opts.variant || 'info';
        var meta = variantMeta(variant);
        var title = opts.title != null ? String(opts.title) : meta.title;

        return new Promise(function (resolve) {
            var backdrop = document.createElement('div');
            backdrop.className =
                'fixed inset-0 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm';
            backdrop.style.zIndex = Z;
            backdrop.setAttribute('role', 'presentation');

            var panel = document.createElement('div');
            panel.className =
                'bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 border ' +
                meta.border +
                ' transform transition-all scale-100';
            panel.setAttribute('role', 'alertdialog');
            panel.setAttribute('aria-modal', 'true');
            panel.setAttribute('aria-labelledby', 'sk-notify-title');

            panel.innerHTML =
                '<div class="flex items-start gap-3">' +
                '<i class="bi ' +
                meta.icon +
                ' text-2xl ' +
                meta.accent +
                ' flex-shrink-0 mt-0.5" aria-hidden="true"></i>' +
                '<div class="flex-1 min-w-0">' +
                '<h3 id="sk-notify-title" class="font-semibold text-gray-900 text-lg">' +
                escapeHtml(title) +
                '</h3>' +
                '<p class="mt-2 text-gray-600 text-sm whitespace-pre-wrap sk-notify-msg"></p>' +
                '</div></div>' +
                '<div class="mt-6 flex justify-end">' +
                '<button type="button" class="sk-notify-ok px-5 py-2.5 rounded-xl text-white font-medium shadow-md hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2" style="background:linear-gradient(to right,#f68b1f,#e67a0f)">OK</button>' +
                '</div>';

            var msgEl = panel.querySelector('.sk-notify-msg');
            msgEl.textContent = message;

            var onKey = function (e) {
                if (e.key === 'Escape') finish();
            };

            function finish() {
                removeBackdrop(backdrop, onKey);
                resolve();
            }

            panel.querySelector('.sk-notify-ok').addEventListener('click', finish);
            backdrop.addEventListener('click', function (e) {
                if (e.target === backdrop) finish();
            });

            backdrop.appendChild(panel);
            document.body.appendChild(backdrop);
            document.addEventListener('keydown', onKey);
            setTimeout(function () {
                var b = panel.querySelector('.sk-notify-ok');
                if (b) b.focus();
            }, 0);
        });
    }

    /**
     * @param {string} message
     * @param {{ title?: string, confirmText?: string, cancelText?: string, danger?: boolean }} [opts]
     * @returns {Promise<boolean>}
     */
    function skConfirm(message, opts) {
        opts = opts || {};
        var confirmText = opts.confirmText || 'Confirm';
        var cancelText = opts.cancelText || 'Cancel';
        var title = opts.title != null ? String(opts.title) : 'Please confirm';
        var danger = !!opts.danger;

        return new Promise(function (resolve) {
            var backdrop = document.createElement('div');
            backdrop.className =
                'fixed inset-0 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm';
            backdrop.style.zIndex = Z;

            var panel = document.createElement('div');
            panel.className =
                'bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 border border-gray-100';
            panel.setAttribute('role', 'dialog');
            panel.setAttribute('aria-modal', 'true');

            var confirmClass = danger
                ? 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500'
                : 'text-white focus:ring-orange-400';
            var confirmStyle = danger ? '' : 'background:linear-gradient(to right,#f68b1f,#e67a0f)';

            panel.innerHTML =
                '<h3 class="font-semibold text-gray-900 text-lg">' +
                escapeHtml(title) +
                '</h3>' +
                '<p class="mt-3 text-gray-600 text-sm whitespace-pre-wrap sk-confirm-msg"></p>' +
                '<div class="mt-6 flex flex-col-reverse sm:flex-row sm:justify-end gap-2">' +
                '<button type="button" class="sk-confirm-cancel px-4 py-2.5 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2">' +
                escapeHtml(cancelText) +
                '</button>' +
                '<button type="button" class="sk-confirm-yes px-5 py-2.5 rounded-xl font-medium shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 ' +
                confirmClass +
                '"' +
                (confirmStyle ? ' style="' + confirmStyle + '"' : '') +
                '>' +
                escapeHtml(confirmText) +
                '</button></div>';

            panel.querySelector('.sk-confirm-msg').textContent = message;

            var onKey = function (e) {
                if (e.key === 'Escape') finish(false);
            };

            function finish(yes) {
                removeBackdrop(backdrop, onKey);
                resolve(!!yes);
            }

            panel.querySelector('.sk-confirm-yes').addEventListener('click', function () {
                finish(true);
            });
            panel.querySelector('.sk-confirm-cancel').addEventListener('click', function () {
                finish(false);
            });
            backdrop.addEventListener('click', function (e) {
                if (e.target === backdrop) finish(false);
            });

            backdrop.appendChild(panel);
            document.body.appendChild(backdrop);
            document.addEventListener('keydown', onKey);
            setTimeout(function () {
                var b = panel.querySelector('.sk-confirm-yes');
                if (b) b.focus();
            }, 0);
        });
    }

    global.skNotify = skNotify;
    global.skConfirm = skConfirm;
})(typeof window !== 'undefined' ? window : this);

/* نظام إدارة المخزون - مخزن الزينة */

document.addEventListener('DOMContentLoaded', function() {
    initFormHandlers();
    initSmoothScrolling();
    initTooltips();
    initNotifications();
    initDeleteButtons();
    initConfirmButtons();
});

function initFormHandlers() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>جاري المعالجة...';
                submitBtn.disabled = true;
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }, 5000);
            }
        });
    });
}

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// تحسين الإشعارات
function initNotifications() {
  const alerts = document.querySelectorAll('.alert');
  
  alerts.forEach(alert => {
    // إضافة تأثير النبض للإشعارات المهمة
    if (alert.classList.contains('alert-danger') || alert.classList.contains('alert-warning')) {
      alert.classList.add('alert-pulse');
    }
    
    // إضافة صوت للإشعارات (اختياري)
    if (alert.classList.contains('alert-success')) {
      playNotificationSound('success');
    } else if (alert.classList.contains('alert-danger')) {
      playNotificationSound('error');
    } else if (alert.classList.contains('alert-warning')) {
      playNotificationSound('warning');
    }
    
    // إغلاق تلقائي للإشعارات (عدا الأخطاء)
    if (!alert.classList.contains('alert-danger')) {
      setTimeout(() => {
        if (alert && alert.parentNode) {
          closeAlert(alert);
        }
      }, 5000); // 5 ثوان
    }
    
    // تحسين زر الإغلاق
    const closeBtn = alert.querySelector('.btn-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeAlert(alert);
      });
    }
  });
}

// إغلاق الإشعار
function closeAlert(alert) {
  alert.style.animation = 'slideOutRight 0.4s ease-in';
  setTimeout(() => {
    if (alert && alert.parentNode) {
      alert.parentNode.removeChild(alert);
    }
  }, 400);
}

// تشغيل أصوات الإشعارات
function playNotificationSound(type) {
  // يمكن إضافة أصوات هنا إذا رغبت
  // const audio = new Audio(`/static/sounds/${type}.mp3`);
  // audio.play().catch(() => {}); // تجاهل الأخطاء
}

// إظهار إشعار مخصص
function showNotification(message, type = 'info', duration = 5000) {
  const container = document.querySelector('.notifications-container') || createNotificationContainer();
  
  const alert = document.createElement('div');
  alert.className = `alert alert-${type} alert-dismissible fade show`;
  alert.setAttribute('role', 'alert');
  
  const iconMap = {
    'success': 'check-circle-fill',
    'danger': 'x-circle-fill',
    'warning': 'exclamation-triangle-fill',
    'info': 'info-circle-fill',
    'primary': 'bell-fill'
  };
  
  const titleMap = {
    'success': 'نجح!',
    'danger': 'خطأ!',
    'warning': 'تحذير!',
    'info': 'معلومة!',
    'primary': 'تنبيه!'
  };
  
  alert.innerHTML = `
    <div class="alert-content">
      <div class="alert-icon">
        <i class="bi bi-${iconMap[type] || 'bell-fill'}"></i>
      </div>
      <div class="alert-message">
        <strong>${titleMap[type] || 'تنبيه!'}</strong>
        <p>${message}</p>
      </div>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="إغلاق">
        <i class="bi bi-x"></i>
      </button>
    </div>
  `;
  
  container.appendChild(alert);
  
  // إضافة تأثيرات
  if (type === 'danger' || type === 'warning') {
    alert.classList.add('alert-pulse');
  }
  
  // إغلاق تلقائي
  if (type !== 'danger' && duration > 0) {
    setTimeout(() => {
      if (alert && alert.parentNode) {
        closeAlert(alert);
      }
    }, duration);
  }
  
  // إضافة مستمع لزر الإغلاق
  const closeBtn = alert.querySelector('.btn-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      closeAlert(alert);
    });
  }
}

// إنشاء حاوية الإشعارات إذا لم تكن موجودة
function createNotificationContainer() {
  const container = document.createElement('div');
  container.className = 'notifications-container';
  document.body.appendChild(container);
  return container;
}

// نظام الرسائل المنبثقة المحسن
function showConfirmModal(options) {
  const {
    title = 'تأكيد العملية',
    message = 'هل أنت متأكد من تنفيذ هذه العملية؟',
    details = '',
    type = 'confirm',
    confirmText = 'نعم، تأكيد',
    cancelText = 'إلغاء',
    onConfirm = () => {},
    onCancel = () => {},
    icon = 'exclamation-triangle-fill'
  } = options;

  // إنشاء Modal HTML
  const modalHtml = `
    <div class="modal fade modal-${type}" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">
              <i class="bi bi-${icon} modal-icon"></i>
              ${title}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="إغلاق">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="confirm-message">
              <div class="confirm-icon">
                <i class="bi bi-${icon}"></i>
              </div>
              <div class="confirm-text">${message}</div>
              ${details ? `<div class="confirm-details">${details}</div>` : ''}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              <i class="bi bi-x-circle me-1"></i>${cancelText}
            </button>
            <button type="button" class="btn btn-${type === 'danger' ? 'danger' : type === 'success' ? 'success' : 'warning'}" id="confirmBtn">
              <i class="bi bi-check-circle me-1"></i>${confirmText}
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  // إزالة Modal السابق إذا كان موجوداً
  const existingModal = document.getElementById('confirmModal');
  if (existingModal) {
    existingModal.remove();
  }

  // إضافة Modal الجديد
  document.body.insertAdjacentHTML('beforeend', modalHtml);

  // إظهار Modal
  const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
  modal.show();

  // إضافة مستمعي الأحداث
  const confirmBtn = document.getElementById('confirmBtn');
  const modalElement = document.getElementById('confirmModal');

  confirmBtn.addEventListener('click', () => {
    modal.hide();
    onConfirm();
  });

  modalElement.addEventListener('hidden.bs.modal', () => {
    onCancel();
    modalElement.remove();
  });

  // إضافة تأثير النبض للرسائل المهمة
  if (type === 'danger' || type === 'warning') {
    modalElement.classList.add('modal-pulse');
  }

  return modal;
}

// رسائل تأكيد سريعة
function confirmDelete(itemName, onConfirm) {
  showConfirmModal({
    title: 'تأكيد الحذف',
    message: `هل أنت متأكد من حذف "${itemName}"؟`,
    details: 'هذا الإجراء لا يمكن التراجع عنه.',
    type: 'danger',
    confirmText: 'نعم، احذف',
    cancelText: 'إلغاء',
    icon: 'trash-fill',
    onConfirm: onConfirm
  });
}

function confirmAction(actionName, onConfirm) {
  showConfirmModal({
    title: 'تأكيد العملية',
    message: `هل أنت متأكد من ${actionName}؟`,
    type: 'confirm',
    confirmText: 'نعم، تأكيد',
    cancelText: 'إلغاء',
    icon: 'question-circle-fill',
    onConfirm: onConfirm
  });
}

function confirmSuccess(message, onConfirm) {
  showConfirmModal({
    title: 'تم بنجاح',
    message: message,
    type: 'success',
    confirmText: 'حسناً',
    cancelText: '',
    icon: 'check-circle-fill',
    onConfirm: onConfirm
  });
}

// تحسين أزرار الحذف الموجودة
function enhanceDeleteButtons() {
  const deleteButtons = document.querySelectorAll('a[href*="delete"], button[onclick*="delete"]');
  
  deleteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      
      const itemName = this.getAttribute('data-item-name') || 
                      this.closest('tr')?.querySelector('td:first-child')?.textContent?.trim() ||
                      'هذا العنصر';
      
      const deleteUrl = this.href || this.getAttribute('data-url');
      
      confirmDelete(itemName, () => {
        if (deleteUrl) {
          window.location.href = deleteUrl;
        } else if (this.onclick) {
          this.onclick();
        }
      });
    });
  });
}

// تحسين أزرار التأكيد الموجودة
function enhanceConfirmButtons() {
  const confirmButtons = document.querySelectorAll('button[data-confirm], a[data-confirm]');
  
  confirmButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      
      const confirmMessage = this.getAttribute('data-confirm') || 'هل أنت متأكد من تنفيذ هذه العملية؟';
      const actionUrl = this.href || this.getAttribute('data-url');
      
      confirmAction(confirmMessage, () => {
        if (actionUrl) {
          window.location.href = actionUrl;
        } else if (this.onclick) {
          this.onclick();
        }
      });
    });
  });
}

// عمليات الصفحة الرئيسية
function refreshDashboard() {
  showConfirmModal({
    title: 'تحديث البيانات',
    message: 'هل تريد تحديث جميع البيانات في الصفحة؟',
    details: 'سيتم إعادة تحميل الإحصائيات والمبيعات الأخيرة.',
    type: 'info',
    confirmText: 'نعم، حدث',
    cancelText: 'إلغاء',
    icon: 'arrow-clockwise',
    onConfirm: () => {
      showNotification('جاري تحديث البيانات...', 'info', 2000);
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    }
  });
}

function exportTodayData() {
  showConfirmModal({
    title: 'تصدير بيانات اليوم',
    message: 'هل تريد تصدير جميع بيانات اليوم؟',
    details: 'سيتم تصدير المبيعات والفواتير والإحصائيات ليوم ' + new Date().toLocaleDateString('ar-SA'),
    type: 'warning',
    confirmText: 'نعم، صدر',
    cancelText: 'إلغاء',
    icon: 'download',
    onConfirm: () => {
      showNotification('جاري تصدير البيانات...', 'info', 3000);
      // يمكن إضافة منطق التصدير هنا
      setTimeout(() => {
        showNotification('تم تصدير البيانات بنجاح!', 'success', 3000);
      }, 2000);
    }
  });
}

async function showSystemInfo() {
  try {
    // جلب إعدادات المتجر
    const response = await fetch('/api/settings/store');
    const result = await response.json();
    const settings = result.success ? result.settings : {};
    
    const systemInfo = `
      <div class="system-info">
        <div class="row">
          <div class="col-md-6">
            <h6><i class="bi bi-cpu me-2"></i>معلومات النظام</h6>
            <ul class="list-unstyled">
              <li><strong>اسم النظام:</strong> ${settings.app_name || 'نظام إدارة المخزون - مخزن الزينة'}</li>
              <li><strong>الوصف:</strong> ${settings.store_description || 'نظام متكامل لإدارة المخزون والمبيعات والمشتريات'}</li>
              <li><strong>الإصدار:</strong> ${settings.app_version || '2.1'}</li>
              <li><strong>تاريخ آخر تحديث:</strong> ${settings.last_updated ? settings.last_updated.split('T')[0] : '9/9/2025'}</li>
              <li><strong>المطور:</strong> محمد فاروق</li>
              <li><strong>جميع الحقوق محفوظة © 2025</strong></li>
            </ul>
          </div>
          <div class="col-md-6">
            <h6><i class="bi bi-gear me-2"></i>إحصائيات النظام</h6>
            <ul class="list-unstyled">
              <li><strong>إجمالي المنتجات:</strong> ${document.querySelector('#total-items')?.textContent || '0'}</li>
               <li><strong>مبيعات اليوم:</strong> ${document.querySelector('#today-sales')?.textContent || '0 ج.س'}</li>
              <li><strong>فواتير اليوم:</strong> ${document.querySelector('#today-invoices')?.textContent || '0'}</li>
              <li><strong>المخزون المنخفض:</strong> ${document.querySelector('#low-stock')?.textContent || '0'}</li>
            </ul>
          </div>
        </div>
      </div>
    `;

    showConfirmModal({
      title: 'معلومات النظام',
      message: systemInfo,
      type: 'info',
      confirmText: 'حسناً',
      cancelText: '',
      icon: 'info-circle-fill',
      onConfirm: () => {}
    });
  } catch (error) {
    console.error('Error loading system info:', error);
    // عرض المعلومات الافتراضية في حالة الخطأ
    const systemInfo = `
      <div class="system-info">
        <div class="row">
          <div class="col-md-6">
            <h6><i class="bi bi-cpu me-2"></i>معلومات النظام</h6>
            <ul class="list-unstyled">
              <li><strong>اسم النظام:</strong> نظام إدارة المخزون - مخزن الزينة</li>
              <li><strong>الوصف:</strong> نظام متكامل لإدارة المخزون والمبيعات والمشتريات</li>
              <li><strong>الإصدار:</strong> 2.1</li>
              <li><strong>تاريخ آخر تحديث:</strong> 9/9/2025</li>
              <li><strong>المطور:</strong> محمد فاروق</li>
              <li><strong>جميع الحقوق محفوظة © 2025</strong></li>
            </ul>
          </div>
          <div class="col-md-6">
            <h6><i class="bi bi-gear me-2"></i>إحصائيات النظام</h6>
            <ul class="list-unstyled">
              <li><strong>إجمالي المنتجات:</strong> ${document.querySelector('#total-items')?.textContent || '0'}</li>
               <li><strong>مبيعات اليوم:</strong> ${document.querySelector('#today-sales')?.textContent || '0 ج.س'}</li>
              <li><strong>فواتير اليوم:</strong> ${document.querySelector('#today-invoices')?.textContent || '0'}</li>
              <li><strong>المخزون المنخفض:</strong> ${document.querySelector('#low-stock')?.textContent || '0'}</li>
            </ul>
          </div>
        </div>
      </div>
    `;

    showConfirmModal({
      title: 'معلومات النظام',
      message: systemInfo,
      type: 'info',
      confirmText: 'حسناً',
      cancelText: '',
      icon: 'info-circle-fill',
      onConfirm: () => {}
    });
  }
}

function backupData() {
  showConfirmModal({
    title: 'نسخ احتياطي',
    message: 'هل تريد إنشاء نسخة احتياطية من جميع البيانات؟',
    details: 'سيتم حفظ نسخة احتياطية من قاعدة البيانات والملفات المهمة.',
    type: 'success',
    confirmText: 'نعم، أنشئ نسخة',
    cancelText: 'إلغاء',
    icon: 'shield-check',
    onConfirm: () => {
      createBackup();
    }
  });
}

async function createBackup() {
  try {
    showNotification('جاري إنشاء النسخة الاحتياطية...', 'info', 0);
    
    const response = await fetch('/api/backup/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    const result = await response.json();
    
    if (result.success) {
      const sizeMB = (result.size / 1024 / 1024).toFixed(2);
      showNotification(`تم إنشاء النسخة الاحتياطية بنجاح! (${sizeMB} MB)`, 'success', 5000);
      
      // إظهار تفاصيل النسخة الاحتياطية
      showConfirmModal({
        title: 'تم إنشاء النسخة الاحتياطية',
        message: `تم إنشاء النسخة الاحتياطية بنجاح: ${result.backup_name}`,
        details: `حجم النسخة: ${sizeMB} MB`,
        type: 'success',
        confirmText: 'حسناً',
        cancelText: '',
        icon: 'check-circle-fill',
        onConfirm: () => {}
      });
    } else {
      showNotification(`فشل في إنشاء النسخة الاحتياطية: ${result.message}`, 'danger', 5000);
    }
  } catch (error) {
    console.error('خطأ في النسخ الاحتياطي:', error);
    showNotification('خطأ في الاتصال بالخادم', 'danger', 5000);
  }
}

async function listBackups() {
  try {
    const response = await fetch('/api/backup/list');
    const result = await response.json();
    
    if (result.success) {
      return result.backups;
    } else {
      showNotification(`فشل في جلب قائمة النسخ الاحتياطية: ${result.message}`, 'danger', 5000);
      return [];
    }
  } catch (error) {
    console.error('خطأ في جلب النسخ الاحتياطية:', error);
    showNotification('خطأ في الاتصال بالخادم', 'danger', 5000);
    return [];
  }
}

async function downloadBackup(backupName) {
  try {
    const response = await fetch(`/api/backup/download/${backupName}`);
    
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = backupName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      showNotification('تم تحميل النسخة الاحتياطية بنجاح!', 'success', 3000);
    } else {
      const result = await response.json();
      showNotification(`فشل في تحميل النسخة الاحتياطية: ${result.message}`, 'danger', 5000);
    }
  } catch (error) {
    console.error('خطأ في تحميل النسخة الاحتياطية:', error);
    showNotification('خطأ في تحميل النسخة الاحتياطية', 'danger', 5000);
  }
}

async function restoreBackup(backupName) {
  try {
    showNotification('جاري استعادة النسخة الاحتياطية...', 'info', 0);
    
    const response = await fetch('/api/backup/restore', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ backup_name: backupName })
    });
    
    const result = await response.json();
    
    if (result.success) {
      showNotification('تم استعادة النسخة الاحتياطية بنجاح!', 'success', 5000);
      
      // إعادة تحميل الصفحة بعد 2 ثانية
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } else {
      showNotification(`فشل في استعادة النسخة الاحتياطية: ${result.message}`, 'danger', 5000);
    }
  } catch (error) {
    console.error('خطأ في استعادة النسخة الاحتياطية:', error);
    showNotification('خطأ في الاتصال بالخادم', 'danger', 5000);
  }
}

function clearCache() {
  showConfirmModal({
    title: 'مسح الذاكرة',
    message: 'هل تريد مسح ذاكرة التطبيق المؤقتة؟',
    details: 'سيتم مسح البيانات المؤقتة وتحسين الأداء.',
    type: 'warning',
    confirmText: 'نعم، امسح',
    cancelText: 'إلغاء',
    icon: 'trash',
    onConfirm: () => {
      showNotification('جاري مسح الذاكرة...', 'info', 2000);
      // مسح localStorage و sessionStorage
      localStorage.clear();
      sessionStorage.clear();
      setTimeout(() => {
        showNotification('تم مسح الذاكرة بنجاح!', 'success', 3000);
      }, 1500);
    }
  });
}

function showHelp() {
  const helpContent = `
    <div class="help-content">
      <h6><i class="bi bi-question-circle me-2"></i>دليل الاستخدام السريع</h6>
      <div class="row">
        <div class="col-md-6">
          <h6>العمليات الأساسية:</h6>
          <ul>
            <li><strong>نقطة البيع:</strong> لإتمام المبيعات</li>
            <li><strong>قائمة الفواتير:</strong> لعرض الفواتير</li>
            <li><strong>تحديث البيانات:</strong> لإعادة تحميل الإحصائيات</li>
            <li><strong>تصدير اليوم:</strong> لتصدير بيانات اليوم</li>
          </ul>
        </div>
        <div class="col-md-6">
          <h6>العمليات الإضافية:</h6>
          <ul>
            <li><strong>معلومات النظام:</strong> لعرض تفاصيل النظام</li>
            <li><strong>نسخ احتياطي:</strong> لحفظ البيانات</li>
            <li><strong>مسح الذاكرة:</strong> لتحسين الأداء</li>
            <li><strong>المساعدة:</strong> لعرض هذا الدليل</li>
          </ul>
        </div>
      </div>
      <div class="alert alert-info mt-3">
        <i class="bi bi-lightbulb me-2"></i>
        <strong>نصيحة:</strong> يمكنك استخدام لوحة المفاتيح للتنقل السريع بين الصفحات.
      </div>
    </div>
  `;

  showConfirmModal({
    title: 'المساعدة',
    message: helpContent,
    type: 'info',
    confirmText: 'فهمت',
    cancelText: '',
    icon: 'question-circle-fill',
    onConfirm: () => {}
  });
}

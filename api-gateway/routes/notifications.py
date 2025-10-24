# أكمل من آخر نقطة...
@router.post("/rules", response_model=NotificationRule)
async def create_notification_rule(
    rule_data: RuleCreateRequest,
    user: dict = Depends()
):
    """
    إنشاء قاعدة إشعار جديدة
    """
    try:
        # TODO: حفظ القاعدة في قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return NotificationRule(
            id=1,
            name=rule_data.name,
            condition=rule_data.condition,
            action=rule_data.action,
            is_active=rule_data.is_active,
            created_at="2024-01-01T00:00:00Z"
        )
        
    except Exception as e:
        logger.error(f"Create notification rule error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء إنشاء قاعدة الإشعار")

@router.put("/rules/{rule_id}", response_model=NotificationRule)
async def update_notification_rule(
    rule_id: int,
    rule_data: RuleCreateRequest,
    user: dict = Depends()
):
    """
    تحديث قاعدة إشعار
    """
    try:
        # TODO: تحديث القاعدة في قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        if rule_id == 1:
            return NotificationRule(
                id=1,
                name=rule_data.name,
                condition=rule_data.condition,
                action=rule_data.action,
                is_active=rule_data.is_active,
                created_at="2024-01-01T00:00:00Z"
            )
        else:
            raise HTTPException(status_code=404, detail="القاعدة غير موجودة")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update notification rule error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء تحديث قاعدة الإشعار")

@router.delete("/rules/{rule_id}")
async def delete_notification_rule(rule_id: int, user: dict = Depends()):
    """
    حذف قاعدة إشعار
    """
    try:
        # TODO: حذف القاعدة من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        if rule_id == 1:
            return {"message": "تم حذف القاعدة بنجاح"}
        else:
            raise HTTPException(status_code=404, detail="القاعدة غير موجودة")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete notification rule error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء حذف قاعدة الإشعار")

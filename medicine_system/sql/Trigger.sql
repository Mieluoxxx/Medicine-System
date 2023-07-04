use flask;
-- 订单的销售和退货会直接影响库存量
CREATE TRIGGER update_stock
    AFTER INSERT
    ON Orderlist
    FOR EACH ROW
BEGIN
    IF NEW.type = '销售' THEN
        UPDATE Medicine
        SET stock = stock - NEW.quantity
        WHERE id = NEW.m_id;
    ELSEIF NEW.type = '退货' THEN
        UPDATE Medicine
        SET stock = stock + NEW.quantity
        WHERE id = NEW.m_id;
    END IF;
END;

-- 采购单的和退货会直接影响库存量
CREATE TRIGGER update_stock2
    AFTER INSERT
    ON Purchase
    FOR EACH ROW
BEGIN
    IF NEW.type = '采购' THEN
        UPDATE Medicine
        SET stock = stock - NEW.quantity
        WHERE id = NEW.medicine_id;
    ELSEIF NEW.type = '退货' THEN
        UPDATE Medicine
        SET stock = stock + NEW.quantity
        WHERE id = NEW.medicine_id;
    END IF;
END;


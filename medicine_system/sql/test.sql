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

-- 求药品最新的单价
SELECT DISTINCT m_id, name, cost, price
FROM (
    SELECT p.m_id, m.name, p.cost, p.price,
           ROW_NUMBER() OVER (PARTITION BY m_id ORDER BY date DESC) AS rn
    FROM price p
    Left outer join medicine m ON m.id = p.m_id
) t
WHERE rn = 1
ORDER BY m_id;

SELECT Orderlist.date,
COALESCE(SUM(Orderlist.quantity * 售价), 0) AS 销售额,
COALESCE(SUM(Orderlist.quantity * 售价 - Orderlist.quantity * 成本), 0) AS 利润
FROM Orderlist
LEFT JOIN Medicine ON Orderlist.m_id = Medicine.id
LEFT JOIN Purchase ON Medicine.id = Purchase.medicine_id AND Purchase.date = Orderlist.date
WHERE Orderlist.type != '退货' AND Orderlist.is_returned != 1
GROUP BY Orderlist.date;

-- 求每一天的利润
SELECT o.date, ROUND(SUM(o.quantity * price), 2) AS sales
FROM (
    SELECT o.m_id, o.date, o.quantity,
        (SELECT price FROM Price WHERE m_id = o.m_id AND date <= o.date ORDER BY date DESC LIMIT 1) AS price
    FROM Orderlist o
) AS o
GROUP BY o.date;
